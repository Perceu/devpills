# DevPills — Agent Guide

## What this is

Generates 1080×1440 Instagram post images from code snippets. Each post = `{name}_post.png` + `{name}_capa.png` (cover) in `build/`.

Stack: Python, Pillow, Pygments, Typer. No tests, no linters, no formatters, no CI.

## Commands

| Command | What it does |
|---|---|
| `python run.py render-python <post_name>` | Render a Python post |
| `python run.py render-php <post_name>` | Render a PHP post |
| `python run.py render-lua <post_name>` | Render a Lua post |
| `python run.py render-go <post_name>` | Render a Go post |
| `python run.py render-rust <post_name>` | Render a Rust post |
| `python run.py render-bun <post_name>` | Render a Bun/TS post |
| (add `--light` to any command) | Use light theme (Visual Studio) instead of dark (Dracula) |
| `python publish.py` | List all posts and publish status |
| `python publish.py run [--light|--dark] [--dry-run]` | Render + publish next pending post to Instagram |
| `python publish.py next` | Preview the next post (caption + image) |

Render commands exist for each language in `posts/{lang}/` — same pattern. Credentials via env vars `INSTA_USER` / `INSTA_PASS` or prompted. Published state tracked in `.published.json`.

## Architecture

- **`run.py`** — Typer CLI entrypoint. Each command looks up `posts/{lang}/{name}.{ext}` (single file) or `posts/{lang}/{name}/` (directory → one image per file).
- **`generator/main.py`** — `Pub` class reads source code, syntax-highlights via Pygments `ImageFormatter`, saves to `build/codigo.png` temporarily, then delegates to a template.
- **`generator/templates/polaroid{Language}.py`** — One per language. Each has `run()` → `generate()` (post card) + `generate_cape()` (cover card). Implements `get_logo()` (language icon from `statics/`).
- **`generator/settings.py`** — Constants: 1080×1440, Fira Code font, Dracula Pygments theme, paths to statics.
- **`generator/helpers.py`** — `DrawHelpers` (text dimensions, hex color inversion).

## Content conventions

- Code files live under `posts/{language}/`. Max 30 lines.
- First lines are docstring comments (title/description — Instagram caption source).
- Directory mode: files starting with `__` are skipped; output gets numeric suffix (e.g. `mqtt0_post.png`).
- Signature on every card: `@perceubertoletti.dev`
- Output to `build/{lang}_{name}_post.png` / `build/{lang}_{name}_capa.png` (e.g. `go_variaveis_post.png`).

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Adding a new language

1. Add logo PNG to `statics/` and constant in `generator/settings.py`.
2. Create `generator/templates/polaroid{Language}.py` — subclass the polaroid pattern (signature, `get_logo()`, `generate()`, `generate_cape()`, `run()`).
3. Add command to `run.py` following the existing pattern.
4. Add directory `posts/{language}/`.
