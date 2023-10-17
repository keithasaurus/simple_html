from html import escape
from types import GeneratorType
from typing import TYPE_CHECKING, cast, List

from simple_html.nodes import Node, TagTuple, SafeString, Tag


def _render(node: Node, strs: List[str]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    if type(node) is tuple:
        if len(node) == 3:
            if TYPE_CHECKING:
                node = cast(TagTuple, node)
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
    elif isinstance(node, Tag):
        strs.append(node.rendered)
    elif isinstance(node, list):
        for n in node:
            _render(n, strs)
    elif isinstance(node, GeneratorType):
        for n in node:
            _render(n, strs)
    else:
        raise TypeError(f"Got unknown type: {type(node)}")


def render(node: Node) -> str:
    result_strs: List[str] = []
    stack = [node]
    while stack:
        node = stack.pop(0)
        if isinstance(node, tuple):
            if len(node) == 3:
                if TYPE_CHECKING:
                    node = cast(Tag, node)
                # Tag
                result_strs.append(node[0])
                stack.insert(0, (node[2],))
                for c in node[1][::-1]:
                    stack.insert(0, c)
            else:
                if TYPE_CHECKING:
                    node = cast(SafeString, node)
                result_strs.append(node[0])
        elif isinstance(node, str):
            result_strs.append(escape(node))
        elif isinstance(node, Tag):
            result_strs.append(node.rendered)
        elif isinstance(node, list):
            for c in node[::-1]:
                stack.insert(0, c)
        elif isinstance(node, GeneratorType):
            for c in list(node)[::-1]:
                stack.insert(0, c)
        else:
            raise TypeError(
                "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
            )
    return "".join(result_strs)


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"<!doctype {doc_type_details}>{render(node)}"
