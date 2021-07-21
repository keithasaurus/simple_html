from html import escape
from simple_html.nodes import Node, SafeString, Tag


def render_tag(tag: Tag) -> str:
    tag_start = f"<{tag.name}"
    if len(tag.attributes) > 0:
        attrs = " ".join([f'{key}="{val}"' for key, val in tag.attributes])
        tag_with_attrs: str = f"{tag_start} {attrs}"
    else:
        tag_with_attrs = tag_start

    if len(tag.children) > 0:
        children_str = "".join([render_node(node) for node in tag.children])

        return f"{tag_with_attrs}>{children_str}</{tag.name}>"
    else:
        if tag.self_closes:
            return f"{tag_with_attrs}/>"
        else:
            return f"{tag_with_attrs}></{tag.name}>"


def render_node(node: Node) -> str:
    if isinstance(node, Tag):
        return render_tag(node)
    elif isinstance(node, str):
        return escape(node)
    elif isinstance(node, SafeString):
        return node.safe_val
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )
