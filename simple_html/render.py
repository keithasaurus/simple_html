from html import escape

from simple_html.nodes import FlatGroup, Node, SafeString, Tag, TagBase


def doctype(details: str) -> str:
    return f"<!doctype {details}>"


def render_tag_base(tag: TagBase) -> str:
    if tag.self_closes:
        return f"<{tag.name}/>"
    else:
        return f"<{tag.name}></{tag.name}>"


def render_tag(tag: Tag) -> str:
    tag_base = tag.tag_base
    if tag.attributes:
        attrs_ = " ".join([
            key if val is None else f'{key}="{val}"'
            for key, val in tag.attributes.items()
        ])
    else:
        attrs_ = None

    if tag.children:
        children_str = "".join([render(node) for node in tag.children])
        if tag.attributes:
            return f"<{tag_base.name} {attrs_}>{children_str}</{tag_base.name}>"
        else:
            return f"<{tag_base.name}>{children_str}</{tag_base.name}>"

    elif tag.attributes:
        if tag_base.self_closes:
            return f"<{tag_base.name} {attrs_}/>"
        else:
            return f"<{tag_base.name} {attrs_}></{tag_base.name}>"
    else:
        return render_tag_base(tag_base)


def render(node: Node) -> str:
    # note that the first two checks here are so much faster than the isinstance
    # checks that it's still better to put them first, even if they aren't the most common
    if type(node) is tuple:
        # SafeString
        return node[0]
    elif node is None:
        return ""
    elif isinstance(node, Tag):
        return render_tag(node)
    elif isinstance(node, str):
        return escape(node)
    elif isinstance(node, FlatGroup):
        return "".join([render(n) for n in node.nodes])
    elif isinstance(node, TagBase):
        return render_tag_base(node)
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"{doctype(doc_type_details)}{render(node)}"
