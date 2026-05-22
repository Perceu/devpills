import os
import re
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import typer
from PIL import Image
from instagrapi import Client

load_dotenv()

POSTS_DIR = Path("posts")
BUILD_DIR = Path("build")
TRACKER_FILE = Path(".published.json")
HASHTAGS = "#devpills #programacao #python #php #rust #go #lua #typescript"
SIGNATURE = "@perceubertoletti.dev"

app = typer.Typer()

LANG_CONFIG = {
    "python": {"ext": ".py"},
    "php": {"ext": ".php"},
    "lua": {"ext": ".lua"},
    "go": {"ext": ".go"},
    "rust": {"ext": ".rs"},
    "bun": {"ext": ".ts"},
}


def load_tracker():
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text())
    return {}


def save_tracker(data):
    TRACKER_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def extract_caption(src_path):
    text = src_path.read_text()

    for pattern in [r'"""(.+?)"""', r"'''(.+?)'''", r'/\*(.+?)\*/']:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            lines = [re.sub(r'^[ *]+', '', l).strip() for l in m.group(1).strip().split('\n') if l.strip()]
            return '\n'.join(lines)

    m = re.search(r'--\[\[(.+?)\]\]', text, re.DOTALL)
    if m:
        lines = [l.strip() for l in m.group(1).strip().split('\n') if l.strip()]
        return '\n'.join(lines)

    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('-- '):
            lines.append(line[3:])
        elif line.startswith('# '):
            lines.append(line[2:])
        elif line.startswith('// '):
            lines.append(line[3:])
        else:
            break
    if lines:
        return '\n'.join(lines)

    return src_path.stem


def make_post(lang, name, src_path, tracker):
    key = str(src_path.relative_to(POSTS_DIR))
    prefix = f"{lang}_"
    img_post = BUILD_DIR / f"{prefix}{name}_post.png"
    img_capa = BUILD_DIR / f"{prefix}{name}_capa.png"
    entry = tracker.get(key, {})
    return {
        "key": key,
        "lang": lang,
        "name": name,
        "src": src_path,
        "img": img_post if img_post.exists() else None,
        "capa": img_capa if img_capa.exists() else None,
        "caption": extract_caption(src_path),
        "published": entry.get("published", False),
        "published_at": entry.get("published_at", ""),
    }


def find_posts():
    tracker = load_tracker()
    posts = []

    for lang_dir in sorted(POSTS_DIR.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name.startswith("."):
            continue
        lang = lang_dir.name

        for f in sorted(lang_dir.iterdir()):
            if f.name.startswith("__") or f.name.startswith("sample"):
                continue
            if f.is_dir():
                continue
            ext = f.suffix.lower()
            if ext not in {".py", ".php", ".lua", ".go", ".rs", ".ts"}:
                continue
            posts.append(make_post(lang, f.stem, f, tracker))

    posts.sort(key=lambda p: (p["published_at"] or "z", p["key"]))
    return posts


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        list_posts()


def list_posts():
    posts = find_posts()
    published = [p for p in posts if p["published"]]
    pending = [p for p in posts if not p["published"]]

    typer.echo(f"Total: {len(posts)} | Published: {len(published)} | Pending: {len(pending)}")

    if pending:
        typer.echo("\n── Pending ──")
        for p in pending:
            img = "✓" if p["img"] else "✗"
            typer.echo(f"  [{img}] {p['key']}")

    if published:
        typer.echo("\n── Published ──")
        for p in published:
            typer.echo(f"  [✓] {p['key']} ({p['published_at']})")


@app.command()
def next():
    posts = find_posts()
    pending = [p for p in posts if not p["published"]]

    if not pending:
        typer.echo("All posts published!")
        raise typer.Exit()

    post = pending[0]
    typer.echo(f"Next: {post['key']}")
    if post["img"] and post["capa"]:
        typer.echo(f"Cover: {post['capa']}")
        typer.echo(f"Code:  {post['img']}")
    else:
        typer.echo("⚠ Not rendered yet — will render before publishing")
    typer.echo(f"\nCaption:\n{post['caption']}")


@app.command()
def run(
    username: str = typer.Option(None, "--user", envvar="INSTA_USER", help="Instagram username"),
    password: str = typer.Option(None, "--pass", envvar="INSTA_PASS", hide_input=True, help="Instagram password"),
    light: bool = typer.Option(False, "--light", help="Use light theme"),
    dark: bool = typer.Option(False, "--dark", help="Use dark theme"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without posting"),
):
    if light and dark:
        typer.echo("Use --light or --dark, not both")
        raise typer.Exit(1)

    if not username:
        username = typer.prompt("Instagram username")
    if not password:
        password = typer.prompt("Instagram password", hide_input=True)

    posts = find_posts()
    pending = [p for p in posts if not p["published"]]

    if not pending:
        typer.echo("All posts published!")
        raise typer.Exit()

    post = pending[0]
    typer.echo(f"Publishing: {post['key']}")

    needs_render = not post["img"] or not post["capa"]
    if light or dark:
        needs_render = True

    if needs_render:
        typer.echo("Rendering...")
        cmd = [sys.executable, "run.py", f"render-{post['lang']}", post["name"]]
        if light:
            cmd.append("--light")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            typer.echo(f"Render failed:\n{r.stderr}")
            raise typer.Exit(1)
        prefix = f"{post['lang']}_"
        post["img"] = BUILD_DIR / f"{prefix}{post['name']}_post.png"
        post["capa"] = BUILD_DIR / f"{prefix}{post['name']}_capa.png"
        if not post["img"].exists() or not post["capa"].exists():
            typer.echo("Render completed but images not found")
            raise typer.Exit(1)
        typer.echo("Render OK")

    caption = f"{post['caption']}\n.\n{post['key']}\n.\n{SIGNATURE}\n{HASHTAGS}"

    if dry_run:
        typer.echo(f"\nWould post as carousel:\n  Cover: {post['capa']}\n  Code:  {post['img']}\n  Caption:\n{caption}")
        raise typer.Exit()

    typer.echo("Logging in...")
    cl = Client()
    try:
        cl.login(username, password)
    except Exception as e:
        typer.echo(f"Login failed: {e}")
        raise typer.Exit(1)

    typer.echo("Converting images to RGB...")
    upload_paths = []
    for src in [post["capa"], post["img"]]:
        rgb_path = src.with_suffix(".rgb.png")
        Image.open(str(src)).convert("RGB").save(str(rgb_path))
        upload_paths.append(str(rgb_path))

    typer.echo("Uploading carousel...")
    try:
        cl.album_upload(
            paths=upload_paths,
            caption=caption,
        )
    except Exception as e:
        typer.echo(f"Upload failed: {e}")
        raise typer.Exit(1)
    finally:
        for p in upload_paths:
            Path(p).unlink(missing_ok=True)

    tracker = load_tracker()
    tracker[post["key"]] = {
        "published": True,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    save_tracker(tracker)
    typer.echo("Published! ✓")


@app.command()
def mark(post_name: str = typer.Argument(..., help="Post key like go/funcoes.go")):
    tracker = load_tracker()
    if post_name not in tracker:
        tracker[post_name] = {}
    tracker[post_name]["published"] = True
    tracker[post_name]["published_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_tracker(tracker)
    typer.echo(f"Marked {post_name} as published")


if __name__ == "__main__":
    app()
