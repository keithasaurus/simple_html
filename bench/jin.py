import sys
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

sys.path.append(str(Path(__file__).parent))

env = Environment(loader=PackageLoader("jinja_example"), autoescape=select_autoescape())

hello_world_template = env.get_template("hello_world.html")


def hello_world_empty(objs) -> None:
    for _ in objs:
        hello_world_template.render()


basic_template = env.get_template("basic.html")


def basic(objs: list[tuple[str, str, list[str]]]) -> None:
    for obj in objs:
        basic_template.render(
            title=obj[0],
            content=obj[1],
            oks=[obj[2]]
        )
