from html import escape
from simple_html.nodes import Node, SafeString, TagProtocol


def render_tag(tag: TagProtocol) -> str:
    # todo: rewrite with while loop to avoid recursion limit
    tag_start = f"<{tag.name}"
    attrs = " ".join([f'{key}="{val}"' for key, val in tag.attrs])

    tag_with_attrs = tag_start if len(attrs) == 0 else f"{tag_start} {attrs}"

    if len(tag.nodes) > 0:
        children_str = "".join([render_node(node) for node in tag.nodes])

        return f"{tag_with_attrs}>{children_str}</{tag.name}>"
    else:
        if tag.self_closes:
            return f"{tag_with_attrs}/>"
        else:
            return f"{tag_with_attrs}></{tag.name}>"


def escape_str(val: str) -> str:
    return escape(val)


def render_node(node: Node) -> str:
    if isinstance(node, TagProtocol):
        return render_tag(node)
    elif isinstance(node, str):
        return escape(node)
    elif isinstance(node, SafeString):
        return node.safe_val
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )
