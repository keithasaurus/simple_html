from typing import List

from dominate.tags import h1


def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        h1("Hello, World!").render()
