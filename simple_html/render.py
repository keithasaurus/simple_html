from html import escape
from typing import List, Literal

from simple_html.nodes import FlatGroup, Node, SafeString, Tag, TagBase


def doctype(details: str) -> str:
    return f"<!doctype {details}>"


def render_tag_base(tag: TagBase) -> str:
    if tag.self_closes:
        return f"<{tag.name}/>"
    else:
        return f"<{tag.name}></{tag.name}>"


def render_with_doctype(node: Node, doc_type_details: str = "html") -> str:
    return f"{doctype(doc_type_details)}{render(node)}"


def render(node: Node) -> str:
    if isinstance(node, (Tag, FlatGroup)):
        stack: List[Node | tuple[str]] = [node]
        result_strs = []

        while stack:
            node = stack.pop(0)
            if isinstance(node, FlatGroup):
                for c in node.children[::-1]:
                    stack.insert(0, c)
            elif isinstance(node, Tag):
                if node.children:
                    if node.attributes:
                        attrs_ = " ".join([
                            key if val is None else f'{key}="{val}"'
                            for key, val in node.attributes.items()
                        ])
                        result_strs.append(f"<{node.tag_base.name} {attrs_}>")
                        stack.insert(0, (f"</{node.tag_base.name}>", ) )
                    else:
                        result_strs.append(f"<{node.tag_base.name}>")
                        stack.insert(0, (f"</{node.tag_base.name}>", ))
                elif node.attributes:
                    attrs_ = " ".join([
                        key if val is None else f'{key}="{val}"'
                        for key, val in node.attributes.items()
                    ])
                    if node.tag_base.self_closes:
                        result_strs.append(f"<{node.tag_base.name} {attrs_}/>")
                    else:
                        result_strs.append(
                            f"<{node.tag_base.name} {attrs_}></{node.tag_base.name}>"
                        )
                else:
                    if node.tag_base.self_closes:
                        result_strs.append(f"<{node.tag_base.name}/>")
                    else:
                        result_strs.append(f"<{node.tag_base.name}></{node.tag_base.name}>")

                for c in node.children[::-1]:
                    stack.insert(0, c)
            elif isinstance(node, tuple):
                result_strs.append(node[0])
            else:
                if isinstance(node, str):
                    result_strs.append(escape(node))
                elif node is None:
                    pass
                elif isinstance(node, SafeString):
                    result_strs.append(node.safe_val)
                elif isinstance(node, TagBase):
                    if node.self_closes:
                        result_strs.append(f"<{node.name}/>")
                    else:
                        result_strs.append(f"<{node.name}></{node.name}>")
                else:
                    raise TypeError(
                        "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
                    )

        return "".join(result_strs)
    else:
        return render_leaf(node)


def render_tag_parts(tag: Tag) -> tuple[str, str | None]:
    if tag.children:
        if tag.attributes:
            attrs_ = " ".join([
                key if val is None else f'{key}="{val}"'
                for key, val in tag.attributes.items()
            ])
            return f"<{tag.tag_base.name} {attrs_}>", f"</{tag.tag_base.name}>"
        else:
            return f"<{tag.tag_base.name}>", f"</{tag.tag_base.name}>"
    elif tag.attributes:
        attrs_ = " ".join([
            key if val is None else f'{key}="{val}"'
            for key, val in tag.attributes.items()
        ])
        if tag.tag_base.self_closes:
            return f"<{tag.tag_base.name} {attrs_}/>", None
        else:
            return f"<{tag.tag_base.name} {attrs_}></{tag.tag_base.name}>", None
    else:
        if tag.tag_base.self_closes:
            return f"<{tag.tag_base.name}/>", None
        else:
            return f"<{tag.tag_base.name}></{tag.tag_base.name}>", None


def render_leaf(node: str | None | SafeString | TagBase) -> str:
    if isinstance(node, str):
        return escape(node)
    elif node is None:
        return ""
    elif isinstance(node, SafeString):
        return node.safe_val
    elif isinstance(node, TagBase):
        if node.self_closes:
            return f"<{node.name}/>"
        else:
            return f"<{node.name}></{node.name}>"
    else:
        raise TypeError(
            "Expected `Tag`, `SafeString` or `str` but got `{}`".format(type(node))
        )
