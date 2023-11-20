from typing import List

from fast_html import h1, render


def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        render(h1("Hello, World!"))
