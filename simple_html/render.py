from html import escape

from simple_html.doctype import doctype
from simple_html.nodes import Node, SafeString, Tag, TagBase


def render_tag(tag: Tag) -> str:
    tag_start = f"<{tag.tag_base.name}"
    if len(tag.attributes) > 0:
        attrs = " ".join([
            key if val is None else f'{key}="{val}"'
            for key, val in tag.attributes
        ])
        tag_with_attrs: str = f"{tag_start} {attrs}"
    else:
        tag_with_attrs = tag_start

    if len(tag.children) > 0:
        children_str = "".join([render(node) for node in tag.children])

        return f"{tag_with_attrs}>{children_str}</{tag.tag_base.name}>"
    else:
        if tag.tag_base.self_closes:
            return f"{tag_with_attrs}/>"
        else:
            return f"{tag_with_attrs}></{tag.tag_base.name}>"


def render(node: Node) -> str:
    if isinstance(node, Tag):
        return render_tag(node)
    if isinstance(node, TagBase):
        if node.self_closes:
            return f"<{node.name}/>"
        else:
            return f"<{node.name}></{node.name}>"
    elif isinstance(node, str):
        return escape(node)
    elif isinstance(node, SafeString):
        return node.safe_val
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"{doctype(doc_type_details)}{render(node)}"
