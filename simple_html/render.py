from html import escape
from typing import cast, TYPE_CHECKING, Dict

from simple_html.nodes import (
    FlatGroup,
    Node,
    Tag,
    TagBase,
    AttrsTag,
    TagNoAttrs,
    SafeStringAlias,
)


def attrs_to_str(attributes: Dict[str, str]) -> str:
    return " ".join(
        [f'{key}="{val}"' if val else key for key, val in attributes.items()]
    )


def render(node: Node) -> str:
    if type(node) is tuple:
        tup_len = len(node)
        if tup_len == 2:
            # TagNoAttrs
            if TYPE_CHECKING:
                node = cast(TagNoAttrs, node)
            children_str = "".join([render(child) for child in node[1]])
            return f"<{node[0].name}>{children_str}</{node[0].name}>"
        elif tup_len == 3:
            if TYPE_CHECKING:
                node = cast(Tag, node)

            tag_base, attributes, children = node
            children_str = "".join([render(child) for child in children])
            return f"<{tag_base.name} {attrs_to_str(attributes)}>{children_str}</{tag_base.name}>"
        else:
            # SafeString
            if TYPE_CHECKING:
                node = cast(SafeStringAlias, node)
            return node[0]
    elif node is None:
        return ""
    elif isinstance(node, str):
        return escape(node)
    elif isinstance(node, AttrsTag):
        tag_base = node.tag_base
        if tag_base.self_closes:
            return f"<{tag_base.name} {attrs_to_str(node.attributes)}/>"
        else:
            return (
                f"<{tag_base.name} {attrs_to_str(node.attributes)}></{tag_base.name}>"
            )
    elif isinstance(node, FlatGroup):
        return "".join([render(n) for n in node.nodes])
    elif isinstance(node, TagBase):
        if node.self_closes:
            return f"<{node.name}/>"
        else:
            return f"<{node.name}></{node.name}>"
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"<!doctype {doc_type_details}>{render(node)}"
