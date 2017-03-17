from html import escape
from simple_html.nodes import SafeString, Tag
from typing import Any


def render_tag(tag: Tag) -> str:
    tag_start = f"<{tag.name}"
    attrs = " ".join([f'{key}="{val}"' for key, val in tag.attrs])

    tag_with_attrs = " ".join([a for a in [tag_start, attrs] if len(a) > 0])

    children_str = "".join([render_node(node) for node in tag.nodes])

    if len(children_str) > 0:
        return f"{tag_with_attrs}>{children_str}</{tag.name}>"
    else:
        return f"{tag_with_attrs}/>"


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
            f'Expected `Tag`, `SafeString` or `str` but got `{type(node)}`'
        )
