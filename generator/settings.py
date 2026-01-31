import os
# from pygments.styles.tango import TangoStyle as Style
# from pygments.styles.vs import VisualStudioStyle as Style
from pygments.styles.dracula import DraculaStyle as Style

class Settings():
    IMAGE_WIDTH = 1080
    IMAGE_HEIGHT = 1440
    SIZE_FONT = 30
    SIZE_FONT_TITLE = 80
    PADDING = 50
    LOAD_TRUNCATED_IMAGES = True
    BASE_PATH = os.getcwd()
    POWERED_BY = f'{BASE_PATH}/statics/powered.png'
    PYTHON_LOGO = f'{BASE_PATH}/statics/python.png'
    PHP_LOGO = f'{BASE_PATH}/statics/php.png'
    BUN_LOGO = f'{BASE_PATH}/statics/bun.png'
    GO_LOGO = f'{BASE_PATH}/statics/go.png'
    RUST_LOGO = f'{BASE_PATH}/statics/rust.png'
    LUA_LOGO = f'{BASE_PATH}/statics/lua.png'
    FONT_FACE = f'{BASE_PATH}/statics/FiraCode.ttf'
    BACKGROUND_RGBA = (0,0,0,255)
    CODE_THEME = Style
