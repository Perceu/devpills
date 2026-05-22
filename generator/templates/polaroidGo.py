
from PIL import Image, ImageDraw, ImageFont
from generator.settings import Settings
from generator.helpers import DrawHelpers


class PolaroidGo():

    signature = "@perceubertoletti.dev"

    def __init__(self, title, image_code, output) -> None:
        self.title = title
        self.img_code = image_code
        self.output = output

    def get_font(self):
        return ImageFont.truetype(Settings.FONT_FACE, Settings.SIZE_FONT)
    
    def get_font_title(self):
        return ImageFont.truetype(Settings.FONT_FACE, Settings.SIZE_FONT_TITLE)
    
    def get_powered_by(self):
        return Image.open(Settings.POWERED_BY).convert('RGBA')
    
    def get_logo(self):
        return Image.open(Settings.GO_LOGO)
    
    def generate(self):
        font = self.get_font()
        powered_by = self.get_powered_by()

        final_image = Image.new('RGBA', (Settings.IMAGE_WIDTH, Settings.IMAGE_HEIGHT), Settings.BACKGROUND_RGBA)       
        draw = ImageDraw.Draw(final_image)

        draw.rounded_rectangle((Settings.PADDING - 25, Settings.PADDING - 25, Settings.IMAGE_WIDTH - Settings.PADDING + 25, Settings.IMAGE_HEIGHT - Settings.PADDING + 25), radius=10, fill='white', outline='#ccc', width=3)
        draw.rounded_rectangle((Settings.PADDING, Settings.PADDING, Settings.IMAGE_WIDTH - Settings.PADDING, Settings.IMAGE_HEIGHT - Settings.PADDING - 100), radius=10, fill=Settings.CODE_THEME.background_color, outline=Settings.CODE_OUTLINE, width=5)
        draw.text((Settings.PADDING+10, Settings.IMAGE_HEIGHT - Settings.PADDING - 100), self.signature, font=font, fill=(100, 100, 100))
        final_image.paste(powered_by, (Settings.IMAGE_WIDTH - Settings.PADDING - 180, Settings.IMAGE_HEIGHT - Settings.PADDING - 90), powered_by)

        # Redimensionar a imagem para caber nas dimensões desejadas
        img_width, img_height = self.img_code.size
        if img_width > Settings.IMAGE_WIDTH - Settings.PADDING * 2:
            ratio = (Settings.IMAGE_WIDTH - 6 - (Settings.PADDING * 2)-5) / img_width
            img_width = int(img_width * ratio)
            img_height = int(img_height * ratio)

        if img_height > Settings.IMAGE_HEIGHT - Settings.PADDING * 2:
            ratio = (Settings.IMAGE_HEIGHT - 6 - (Settings.PADDING * 2)) / img_height
            img_width = int(img_width * ratio)
            img_height = int(img_height * ratio)

        img_code_final = self.img_code.resize((img_width, img_height))

        final_image.paste(img_code_final, (Settings.PADDING+5, Settings.PADDING+5))

        draw.rounded_rectangle((Settings.PADDING, Settings.PADDING, Settings.IMAGE_WIDTH - Settings.PADDING, Settings.IMAGE_HEIGHT - Settings.PADDING - 100), radius=10, outline=Settings.CODE_OUTLINE, width=5)
        final_image.save(f"{self.output}_post.png")

    def generate_cape(self):
        font = self.get_font()
        font_title = self.get_font_title()
        powered_by = self.get_powered_by()

        final_image = Image.new('RGBA', (Settings.IMAGE_WIDTH, Settings.IMAGE_HEIGHT), Settings.BACKGROUND_RGBA)
        draw = ImageDraw.Draw(final_image)
        draw.rounded_rectangle((Settings.PADDING - 25, Settings.PADDING - 25, Settings.IMAGE_WIDTH - Settings.PADDING + 25, Settings.IMAGE_HEIGHT - Settings.PADDING + 25), radius=10, fill='white', outline='#ccc', width=3)
        draw.rounded_rectangle((Settings.PADDING, Settings.PADDING, Settings.IMAGE_WIDTH - Settings.PADDING, Settings.IMAGE_HEIGHT - Settings.PADDING - 100), radius=10, fill=Settings.CODE_THEME.background_color, outline=Settings.CODE_OUTLINE, width=5)
        draw.text((Settings.PADDING+10, Settings.IMAGE_HEIGHT - Settings.PADDING - 100), self.signature, font=font, fill=(100, 100, 100))
        final_image.paste(powered_by, (Settings.IMAGE_WIDTH - Settings.PADDING - 180, Settings.IMAGE_HEIGHT - Settings.PADDING - 90), powered_by)

        draw_cape = ImageDraw.Draw(final_image)
        draw_cape.text((Settings.PADDING+25, Settings.PADDING+25), "Code Snippet", font=font, fill=DrawHelpers.invertColor(Settings.CODE_THEME.background_color))
        text_width, text_height = DrawHelpers.get_text_dimensions(self.title.title(), font_title)
        draw_cape.text(((Settings.IMAGE_WIDTH-text_width)//2, int(Settings.IMAGE_HEIGHT/2)+100), self.title.title(), font=font_title, fill=DrawHelpers.invertColor(Settings.CODE_THEME.background_color))
        logo = self.get_logo()
        width_logo, height_logo = logo.size
        final_image.paste(logo, (int(Settings.IMAGE_WIDTH/2)-int(width_logo/2), int(Settings.IMAGE_HEIGHT/2)-200), logo)
        final_image.save(f"{self.output}_capa.png")
    
    def run(self):
        self.generate()
        self.generate_cape()