from html import escape
from typing import TYPE_CHECKING, cast

from simple_html.nodes import Node, Tag, SafeStringAlias, AttrsTag, FlatGroup, \
    TagBase


def _render(node: Node, strs: list[str]) -> None:
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
            # SafeString
            if TYPE_CHECKING:
                node = cast(SafeStringAlias, node)
            strs.append(node[0])
    elif isinstance(node, str):
        strs.append(escape(node))
    elif isinstance(node, AttrsTag):
        tag_base = node.tag_base
        strs.append(
            f"<{tag_base.name} {node.attributes}/>"
            if tag_base.self_closes
            else f"<{tag_base.name} {node.attributes}></{tag_base.name}>"
        )
    elif isinstance(node, TagBase):
        strs.append(node.rendered)
    elif isinstance(node, FlatGroup):
        for n in node.nodes:
            _render(n, strs)
    elif node is None:
        pass
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )


def render(node: Node) -> str:
    results: list[str] = []
    _render(node, results)

    return "".join(results) if results else ""


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"<!doctype {doc_type_details}>{render(node)}"
