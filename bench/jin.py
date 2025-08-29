import sys
from pathlib import Path
from typing import List, Tuple

from jinja2 import Environment, PackageLoader, select_autoescape

sys.path.append(str(Path(__file__).parent))

env = Environment(loader=PackageLoader("jinja_example"), autoescape=select_autoescape())


_hello_render = env.get_template("hello_world.html").render
def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        _hello_render()

_basic_render = env.get_template("basic.html").render
def basic(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title, content, oks in objs:
        _basic_render(title=title, content=content, oks=oks)


_basic_long_render = env.get_template("basic_long.html").render
def basic_long(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title, content, oks in objs:
        _basic_long_render(title=title, content=content, oks=oks)

_lorem_render = env.get_template("lorem_ipsum.html").render
def lorem_ipsum(titles: List[str]) -> None:
    for t in titles:
        _lorem_render(title=t)


_render_large_page = env.get_template("large_page.html").render
def large_page(titles: List[str]) -> None:
    for t in titles:
        _render_large_page(title=t)
