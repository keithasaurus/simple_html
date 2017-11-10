from html import escape
from simple_html.nodes import SafeString, Tag
from typing import Any


def render_tag(tag: Tag) -> str:
    # todo: rewrite with while loop to avoid recursion limit
    tag_start = "<{}".format(tag.name)
    attrs = " ".join(['{}="{}"'.format(key, val) for key, val in tag.attrs])

    tag_with_attrs = " ".join([a for a in [tag_start, attrs] if len(a) > 0])

    children_str = "".join([render_node(node) for node in tag.nodes])

    if len(children_str) > 0:
        return "{}>{}</{}>".format(tag_with_attrs, children_str, tag.name)
    else:
        if tag.self_closes:
            return "{}/>".format(tag_with_attrs)
        else:
            return "{}></{}>".format(tag_with_attrs, tag.name)


def escape_str(val: str) -> str:
    return escape(val)


def render_node(node: Any) -> str:  # mypy is fucking up union types right now.
    if isinstance(node, Tag):
        return render_tag(node)  # type: ignore
    elif isinstance(node, str):
        return escape(node)
    elif isinstance(node, SafeString):
        return node.safe_val
    else:
        raise TypeError(
            'Expected `Tag`, `SafeString` or `str` but got `{}`'.format(type(node))
        )
