import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from moviepy import ImageClip, AudioClip, concatenate_videoclips
from generator.settings import Settings


CHAR_RATE = 18
FONT_SIZE = 34
LINE_H = 48
CHAR_W = 20
COVER_DUR = 3.0
HOLD_DUR = 3.0
W, H = 1080, 1920
CODE_X, CODE_Y = 80, 300
CODE_W = W - CODE_X * 2


class ReelGenerator:

    def __init__(self, title, code_path, template, lexer, lang="", dark=True):
        self.title = title
        self.code_path = code_path
        self.TemplateClass = template
        self.lexer = lexer
        self.lang = lang
        self.dark = dark
        self._bg_cache = None
        self._static_cache = None

    # ── colour helpers ──────────────────────────────────────────

    def _c(self, ttype):
        style = Settings.CODE_THEME if self.dark else Settings.LIGHT_CODE_THEME
        cur = ttype
        while cur is not None:
            info = style.style_for_token(cur)
            c = info.get('color')
            if c:
                return f'#{c}'
            cur = getattr(cur, 'parent', None)
        return '#f8f8f2' if self.dark else '#000000'

    def _bg(self):
        return '#282a36' if self.dark else '#f5f5f5'

    def _line_no_color(self):
        return '#6272a4' if self.dark else '#6e7681'

    # ── lexing ──────────────────────────────────────────────────

    def _lex(self, code):
        tokens = list(lex(code, self.lexer))
        chars = []
        line = col = 0
        for ttype, value in tokens:
            color = self._c(ttype)
            for ch in value:
                if ch == '\t':
                    col = ((col // 4) + 1) * 4
                    continue
                chars.append({'ch': ch, 'color': color, 'line': line, 'col': col})
                col += 1
                if ch == '\n':
                    line += 1
                    col = 0
        return chars

    # ── static layers (rendered once) ───────────────────────────

    def _make_bg(self):
        top = np.array([13, 17, 23] if self.dark else [255, 255, 255], dtype=np.float32)
        bot = np.array([22, 27, 34] if self.dark else [240, 240, 240], dtype=np.float32)
        arr = np.zeros((H, W, 3), dtype=np.uint8)
        for y in range(H):
            arr[y] = (top * (1 - y / H) + bot * (y / H)).astype(np.uint8)
        return Image.fromarray(arr, 'RGB')

    def _make_static(self, max_line):
        bg = self._make_bg()
        draw = ImageDraw.Draw(bg)

        # code area background (wide enough for line numbers)
        x, y, w, h = CODE_X - 60, CODE_Y - 50, CODE_W + 100, H - CODE_Y - 180
        draw.rounded_rectangle((x, y, x + w, y + h), radius=12, fill=self._bg())
        for dx, c in [(20, '#ff5f56'), (44, '#ffbd2e'), (68, '#27c93f')]:
            draw.ellipse((x + dx, y + 14, x + dx + 12, y + 26), fill=c)

        # line numbers (right-aligned at CODE_X - 15)
        font = ImageFont.truetype(Settings.FONT_FACE, FONT_SIZE)
        for i in range(1, max_line + 1):
            ny = CODE_Y + (i - 1) * LINE_H
            label = str(i)
            tw = int(font.getlength(label))
            draw.text((CODE_X - 15 - tw, ny), label, font=font, fill=self._line_no_color())

        return bg

    def _get_static(self, max_line):
        if self._static_cache is None:
            self._static_cache = self._make_static(max_line)
        return self._static_cache.copy()

    # ── cover ───────────────────────────────────────────────────

    def _cover_frame(self):
        img = self._make_bg()
        draw = ImageDraw.Draw(img)

        logo = self.TemplateClass(self.title, None, '').get_logo()
        if logo.mode == 'RGBA':
            lw, lh = logo.size
            scale = min(300 / lw, 300 / lh)
            nw, nh = int(lw * scale), int(lh * scale)
            logo = logo.resize((nw, nh), Image.LANCZOS)
            img.paste(logo, ((W - nw) // 2, H // 2 - 280), logo)

        font_t = ImageFont.truetype(Settings.FONT_FACE, 72)
        font_s = ImageFont.truetype(Settings.FONT_FACE, 32)
        title = self.title.replace('-', ' ').title()
        tw = int(font_t.getlength(title))
        draw.text(((W - tw) // 2, H // 2 - 40), title, font=font_t, fill='#f8f8f2')
        lang = self.lang.upper()
        lw2 = int(font_s.getlength(lang))
        draw.text(((W - lw2) // 2, H // 2 + 60), lang, font=font_s, fill='#8b949e')
        sig = '@perceubertoletti.dev'
        sw = int(font_s.getlength(sig))
        draw.text(((W - sw) // 2, H - 120), sig, font=font_s, fill='#484f58')

        return img

    # ── audio ───────────────────────────────────────────────────

    def _click_sound(self, sr=44100):
        dur = 0.03
        t = np.linspace(0, dur, int(sr * dur))
        s = np.sin(2 * np.pi * 1200 * t) * 0.3
        s = s + np.sin(2 * np.pi * 2600 * t) * 0.12
        s *= np.exp(-t * 50)
        return s.astype(np.float32)

    def _build_audio(self, n_chars, total_frames, fps, char_times=None, sr=44100):
        tot = int(total_frames / fps * sr)
        audio = np.zeros(tot, dtype=np.float32)
        click = self._click_sound(sr)
        for i in range(n_chars):
            t = char_times[i] if char_times else COVER_DUR + i / fps
            start = int(t * sr)
            end = min(start + len(click), tot)
            audio[start:end] += click[:end - start]
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio /= peak * 1.05
        return AudioClip(lambda t: np.interp(t * sr, np.arange(len(audio)), audio).reshape(-1, 1),
                         duration=total_frames / fps, fps=sr)

    # ── main ────────────────────────────────────────────────────

    def generate(self):
        prev = (Settings.BACKGROUND_RGBA, Settings.CODE_THEME, Settings.CODE_OUTLINE)
        if not self.dark:
            Settings.BACKGROUND_RGBA = Settings.LIGHT_BACKGROUND_RGBA
            Settings.CODE_THEME = Settings.LIGHT_CODE_THEME
            Settings.CODE_OUTLINE = Settings.LIGHT_CODE_OUTLINE

        with open(self.code_path) as f:
            code = f.read()
        chars = self._lex(code)
        n_chars = len(chars)
        max_line = (chars[-1]['line'] if chars else 0) + 5
        fps = 30
        static_base = self._make_static(max_line)
        font = ImageFont.truetype(Settings.FONT_FACE, FONT_SIZE)

        clips = []
        clips.append(ImageClip(np.array(self._cover_frame())).with_duration(COVER_DUR))

        # build typing states (group consecutive frames with same visible count)
        typing_states = []
        for f in range(math.ceil(n_chars * fps / CHAR_RATE) + 2):
            visible = min(n_chars, int(f * CHAR_RATE / fps))
            if not typing_states or typing_states[-1][0] != visible:
                typing_states.append([visible, 1])
            else:
                typing_states[-1][1] += 1

        overlay = Image.new('RGBA', (W, H))
        odraw = ImageDraw.Draw(overlay)
        char_times = []
        typed = 0
        frame_acc = 0

        for visible, dur in typing_states:
            while typed < visible:
                c = chars[typed]
                if c['ch'] != '\n':
                    odraw.text((CODE_X + c['col'] * CHAR_W, CODE_Y + c['line'] * LINE_H),
                               c['ch'], font=font, fill=c['color'])
                char_times.append(COVER_DUR + frame_acc / fps)
                typed += 1

            frame = static_base.copy()
            frame.paste(overlay, (0, 0), overlay)

            if typed < n_chars:
                cur = chars[min(typed, n_chars - 1)]
                cx = CODE_X + cur['col'] * CHAR_W
                cy = CODE_Y + cur['line'] * LINE_H + 4
                ImageDraw.Draw(frame).rectangle((cx, cy, cx + 2, cy + FONT_SIZE - 2), fill='#f8f8f2')

            clips.append(ImageClip(np.array(frame)).with_duration(dur / fps))
            frame_acc += dur

        frame = static_base.copy()
        frame.paste(overlay, (0, 0), overlay)
        clips.append(ImageClip(np.array(frame)).with_duration(HOLD_DUR))

        video = concatenate_videoclips(clips, method="compose")
        total_frames = int(COVER_DUR * fps) + sum(dur for _, dur in typing_states) + int(HOLD_DUR * fps)
        audio = self._build_audio(n_chars, total_frames, fps, char_times or None)
        video = video.with_audio(audio)

        prefix = f"{self.lang}_" if self.lang else ""
        out = f"{Settings.BASE_PATH}/build/{prefix}{self.title}_reel.mp4"
        video.write_videofile(out, fps=fps, logger=None, preset='ultrafast')

        Settings.BACKGROUND_RGBA, Settings.CODE_THEME, Settings.CODE_OUTLINE = prev
        return out
