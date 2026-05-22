from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.formatters import ImageFormatter
from generator.settings import Settings

class Pub():

    def __init__(self, title, post_path, template, lexer, dark=True, lang="") -> None:
        self.title = title
        self.post_path = post_path
        self.template = template
        self.lexer = lexer
        self.dark = dark
        self.lang = lang

    def gerar_img_codigo(self):

        CODE = []
        with open(self.post_path, 'r') as f:
            CODE = f.readlines()
        CODE.append(' ')

        if len(CODE) <= 0 or len(CODE) > 30:
            raise Exception('seu algoritmo deve conter até 30 linhas')

        theme = Settings.CODE_THEME if self.dark else Settings.LIGHT_CODE_THEME
        formatter = ImageFormatter(style=theme, line_number_bg=theme.background_color, font='Fira Code', font_size=Settings.SIZE_FONT)
        code = highlight(''.join(CODE), self.lexer, formatter)

        with open(f'{Settings.BASE_PATH}/build/codigo.png', 'wb') as f:
            f.write(code)
        
        return Image.open(f'{Settings.BASE_PATH}/build/codigo.png')

    def generate(self):
        prev_bg = Settings.BACKGROUND_RGBA
        prev_theme = Settings.CODE_THEME

        if not self.dark:
            Settings.BACKGROUND_RGBA = Settings.LIGHT_BACKGROUND_RGBA
            Settings.CODE_THEME = Settings.LIGHT_CODE_THEME

        img_codigo = self.gerar_img_codigo()
        prefix = f"{self.lang}_" if self.lang else ""
        output = f"{Settings.BASE_PATH}/build/{prefix}{self.title}"
        gerador = self.template(self.title, img_codigo, output)
        gerador.run()

        Settings.BACKGROUND_RGBA = prev_bg
        Settings.CODE_THEME = prev_theme
