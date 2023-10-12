from html import escape
from typing import TYPE_CHECKING, cast

from simple_html.nodes import Node, TagNoAttrs, Tag, SafeStringAlias, AttrsTag, FlatGroup, \
    TagBase


def _render(node: Node, strs: list[str]) -> None:
    """
    mutate a list instead of constantly rendering strings
    """
    if type(node) is tuple:
        tup_len = len(node)
        if tup_len == 2:
            # TagNoAttrs
            if TYPE_CHECKING:
                node = cast(TagNoAttrs, node)
            strs.append(f"<{node[0]}>")
            for child in node[1]:
                _render(child, strs)
            strs.append(f"</{node[0]}>")
        elif tup_len == 3:
            if TYPE_CHECKING:
                node = cast(Tag, node)
            tag_name = node[0]
            strs.append(f"<{tag_name} {node[1]}>")
            for child in node[2]:
                _render(child, strs)
            strs.append(f"</{tag_name}>")
        else:
            # SafeString
            if TYPE_CHECKING:
                node = cast(SafeStringAlias, node)
            strs.append(node[0])
    elif node is None:
        pass
    elif isinstance(node, str):
        strs.append(escape(node))
    elif isinstance(node, AttrsTag):
        tag_base = node.tag_base
        if tag_base.self_closes:
            strs.append(f"<{tag_base.name} {node.attributes}/>")
        else:
            strs.append(
                f"<{tag_base.name} {node.attributes}></{tag_base.name}>"
            )
    elif isinstance(node, FlatGroup):
        for n in node.nodes:
            _render(n, strs)
    elif isinstance(node, TagBase):
        strs.append(node.rendered)
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
