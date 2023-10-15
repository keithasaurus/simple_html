from html import escape
from types import GeneratorType
from typing import TYPE_CHECKING, cast, List

from simple_html.nodes import Node, Tag, SafeString, TagBase


def _render(node: Node, strs: List[str]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    if type(node) is tuple:
        if len(node) == 3:
            if TYPE_CHECKING:
                node = cast(Tag, node)
            strs.append(node[0])
            for child in node[1]:
                _render(child, strs)
            strs.append(node[2])
        else:
            if TYPE_CHECKING:
                node = cast(SafeString, node)
            strs.append(node[0])
    elif isinstance(node, str):
        strs.append(escape(node))
    elif isinstance(node, TagBase):
        strs.append(node.rendered)
    elif isinstance(node, (list, GeneratorType)):
        for n in node:
            _render(n, strs)
    else:
        raise TypeError(f"Got unknown type: {type(node)}")


def render(node: Node) -> str:
    results: List[str] = []
    _render(node, results)

    return "".join(results)


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"<!doctype {doc_type_details}>{render(node)}"
