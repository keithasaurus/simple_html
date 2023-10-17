from html import escape
from types import GeneratorType
from typing import TYPE_CHECKING, cast, List

from simple_html.nodes import Node, SafeString, Tag


def render(node: Node) -> str:
    result_strs: List[str] = []
    stack = [node]
    while stack:
        node = stack.pop()
        if isinstance(node, tuple):
            if len(node) == 3:
                if TYPE_CHECKING:
                    node = cast(Tag, node)
                # Tag
                result_strs.append(node[0])
                stack.append(node[2])
                stack.extend(node[1][::-1])
            else:
                if TYPE_CHECKING:
                    node = cast(SafeString, node)
                result_strs.append(node[0])
        elif isinstance(node, str):
            result_strs.append(escape(node))
        elif isinstance(node, Tag):
            result_strs.append(node.rendered)
        elif isinstance(node, list):
            stack.extend(node[::-1])
        elif isinstance(node, GeneratorType):
            stack.extend(list(node)[::-1])
        else:
            raise TypeError(
                "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
            )
    return "".join(result_strs)


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"<!doctype {doc_type_details}>{render(node)}"
