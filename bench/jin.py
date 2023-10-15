import sys
from pathlib import Path
from typing import List, Tuple

from jinja2 import Environment, PackageLoader, select_autoescape

sys.path.append(str(Path(__file__).parent))

env = Environment(loader=PackageLoader("jinja_example"), autoescape=select_autoescape())


def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        env.get_template("hello_world.html").render()


def basic(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title, content, oks in objs:
        env.get_template("basic.html").render(title=title, content=content, oks=oks)


def basic_long(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title, content, oks in objs:
        env.get_template("basic_long.html").render(
            title=title, content=content, oks=oks
        )


def lorem_ipsum(titles: List[str]) -> None:
    for t in titles:
        env.get_template("lorem_ipsum.html").render(title=t)