from html import escape
from typing import Tuple

from simple_html.attributes import Attribute
from simple_html.nodes import FlatGroup, Node, SafeString, Tag, TagBase


def doctype(details: str) -> str:
    return f"<!doctype {details}>"


def stringify_attributes(attrs: Tuple[Attribute, ...]) -> str:
    return " ".join([key if val is None else f'{key}="{val}"' for key, val in attrs])


def render_tag_base(tag: TagBase) -> str:
    if tag.self_closes:
        return f"<{tag.name}/>"
    else:
        return f"<{tag.name}></{tag.name}>"


def render_tag(tag: Tag) -> str:
    if tag.children:
        children_str = "".join([render(node) for node in tag.children])
        if tag.attributes:
            return f"<{tag.tag_base.name} {stringify_attributes(tag.attributes)}>{children_str}</{tag.tag_base.name}>"
        else:
            return f"<{tag.tag_base.name}>{children_str}</{tag.tag_base.name}>"

    elif tag.attributes:
        return (
            f"<{tag.tag_base.name} {stringify_attributes(tag.attributes)}/>"
            if tag.tag_base.self_closes
            else f"<{tag.tag_base.name} {stringify_attributes(tag.attributes)}></{tag.tag_base.name}>"
        )
    else:
        return render_tag_base(tag.tag_base)


def render(node: Node) -> str:
    if isinstance(node, Tag):
        return render_tag(node)
    elif isinstance(node, str):
        return escape(node)
    elif node is None:
        return ""
    elif isinstance(node, FlatGroup):
        return "".join(render(n) for n in node.nodes)
    elif isinstance(node, SafeString):
        return node.safe_val
    elif isinstance(node, TagBase):
        return render_tag_base(node)
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"{doctype(doc_type_details)}{render(node)}"
