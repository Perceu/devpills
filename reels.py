import os
import typer
from generator.reel import ReelGenerator
from generator.templates.polaroidPython import PolaroidPython
from generator.templates.polaroidLua import PolaroidLua
from generator.templates.polaroidGo import PolaroidGo
from generator.templates.polaroidPhp import PolaroidPhp
from generator.templates.polaroidBun import PolaroidBun
from generator.templates.polaroidRust import PolaroidRust
from pygments.lexers import get_lexer_by_name
from generator.settings import Settings
from pathlib import Path

app = typer.Typer()

@app.command()
def render_bun(post_name: str, light: bool = typer.Option(False, "--light")):
    post_path = f"{Settings.BASE_PATH}/posts/bun/{post_name}.ts"
    path = Path(post_path)
    lexer = get_lexer_by_name('typescript')
    if path.is_file():
        rg = ReelGenerator(post_name, post_path, PolaroidBun, lexer, lang="bun", dark=not light)
        rg.generate()
    else:
        post_path = f"{Settings.BASE_PATH}/posts/bun/{post_name}/"
        for index, file in enumerate(os.listdir(post_path)):
            if file.startswith('__'):
                continue
            rg = ReelGenerator(f"{post_name}{index}", f"{post_path}{file}", PolaroidBun, lexer, lang="bun", dark=not light)
            rg.generate()

@app.command()
def render_python(post_name: str, light: bool = typer.Option(False, "--light")):
    post_path = f"{Settings.BASE_PATH}/posts/python/{post_name}.py"
    path = Path(post_path)
    lexer = get_lexer_by_name('python')
    if path.is_file():
        rg = ReelGenerator(post_name, post_path, PolaroidPython, lexer, lang="python", dark=not light)
        rg.generate()
    else:
        post_path = f"{Settings.BASE_PATH}/posts/python/{post_name}/"
        for index, file in enumerate(os.listdir(post_path)):
            if file.startswith('__'):
                continue
            rg = ReelGenerator(f"{post_name}{index}", f"{post_path}{file}", PolaroidPython, lexer, lang="python", dark=not light)
            rg.generate()

@app.command()
def render_lua(post_name: str, light: bool = typer.Option(False, "--light")):
    post_path = f"{Settings.BASE_PATH}/posts/lua/{post_name}.lua"
    path = Path(post_path)
    lexer = get_lexer_by_name('lua')
    if path.is_file():
        rg = ReelGenerator(post_name, post_path, PolaroidLua, lexer, lang="lua", dark=not light)
        rg.generate()
    else:
        post_path = f"{Settings.BASE_PATH}/posts/lua/{post_name}/"
        for index, file in enumerate(os.listdir(post_path)):
            if file.startswith('__'):
                continue
            rg = ReelGenerator(f"{post_name}{index}", f"{post_path}{file}", PolaroidLua, lexer, lang="lua", dark=not light)
            rg.generate()

@app.command()
def render_php(post_name: str, light: bool = typer.Option(False, "--light")):
    post_path = f"{Settings.BASE_PATH}/posts/php/{post_name}.php"
    path = Path(post_path)
    lexer = get_lexer_by_name('php')
    if path.is_file():
        rg = ReelGenerator(post_name, post_path, PolaroidPhp, lexer, lang="php", dark=not light)
        rg.generate()
    else:
        post_path = f"{Settings.BASE_PATH}/posts/php/{post_name}/"
        for index, file in enumerate(os.listdir(post_path)):
            if file.startswith('__'):
                continue
            rg = ReelGenerator(f"{post_name}{index}", f"{post_path}{file}", PolaroidPhp, lexer, lang="php", dark=not light)
            rg.generate()

@app.command()
def render_go(post_name: str, light: bool = typer.Option(False, "--light")):
    post_path = f"{Settings.BASE_PATH}/posts/go/{post_name}.go"
    path = Path(post_path)
    lexer = get_lexer_by_name('go')
    if path.is_file():
        rg = ReelGenerator(post_name, post_path, PolaroidGo, lexer, lang="go", dark=not light)
        rg.generate()
    else:
        post_path = f"{Settings.BASE_PATH}/posts/go/{post_name}/"
        for index, file in enumerate(os.listdir(post_path)):
            if file.startswith('__'):
                continue
            rg = ReelGenerator(f"{post_name}{index}", f"{post_path}{file}", PolaroidGo, lexer, lang="go", dark=not light)
            rg.generate()

@app.command()
def render_rust(post_name: str, light: bool = typer.Option(False, "--light")):
    post_path = f"{Settings.BASE_PATH}/posts/rust/{post_name}.rs"
    path = Path(post_path)
    lexer = get_lexer_by_name('rust')
    if path.is_file():
        rg = ReelGenerator(post_name, post_path, PolaroidRust, lexer, lang="rust", dark=not light)
        rg.generate()
    else:
        post_path = f"{Settings.BASE_PATH}/posts/rust/{post_name}/"
        for index, file in enumerate(os.listdir(post_path)):
            if file.startswith('__'):
                continue
            rg = ReelGenerator(f"{post_name}{index}", f"{post_path}{file}", PolaroidRust, lexer, lang="rust", dark=not light)
            rg.generate()

if __name__ == "__main__":
    app()
