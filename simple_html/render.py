from types import GeneratorType
from typing import Iterable, Callable

from simple_html.typedefs import Node, SafeString, Tag
from simple_html.utils import faster_escape, _common_safe_css_props


def _render(nodes: Iterable[Node], append_to_list: Callable[[str], None]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    for node in nodes:
        if type(node) is tuple:
            append_to_list(node[0])
            _render(node[1], append_to_list)
            append_to_list(node[2])
        elif isinstance(node, SafeString):
            append_to_list(node.safe_str)
        elif isinstance(node, str):
            append_to_list(faster_escape(node))
        elif isinstance(node, Tag):
            append_to_list(node.rendered)
        elif isinstance(node, list):
            _render(node, append_to_list)
        elif isinstance(node, GeneratorType):
            _render(node, append_to_list)
        else:
            raise TypeError(f"Got unknown type: {type(node)}")


def render_styles(
    styles: dict[str | SafeString, str | int | float | SafeString]
) -> SafeString:
    ret = ""
    for k, v in styles.items():
        if k not in _common_safe_css_props:
            if isinstance(k, SafeString):
                k = k.safe_str
            else:
                k = faster_escape(k)

        if isinstance(v, SafeString):
            v = v.safe_str
        elif isinstance(v, str):
            v = faster_escape(v)
        # note that ints and floats pass through these condition checks

        ret += f"{k}:{v};"

    return SafeString(ret)


def render(*nodes: Node) -> str:
    results: list[str] = []
    _render(nodes, results.append)

    return "".join(results)
