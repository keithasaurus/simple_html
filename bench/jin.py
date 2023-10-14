import sys
from pathlib import Path
from typing import List

from jinja2 import Environment, PackageLoader, select_autoescape

sys.path.append(str(Path(__file__).parent))

env = Environment(loader=PackageLoader("jinja_example"), autoescape=select_autoescape())


def hello_world_empty(objs: list[None]) -> None:
    for _ in objs:
        env.get_template("hello_world.html").render()


def basic(objs: List[tuple[str, str, List[str]]]) -> None:
    for title, content, oks in objs:
        env.get_template("basic.html").render(title=title, content=content, oks=oks)


def basic_long(objs: List[tuple[str, str, List[str]]]) -> None:
    for title, content, oks in objs:
        env.get_template("basic_long.html").render(
            title=title, content=content, oks=oks
        )
