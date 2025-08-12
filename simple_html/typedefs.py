from typing import Any, Union, Generator

from simple_html.utils import _common_safe_attribute_names, escape_attribute_key, faster_escape


class SafeString:
    def __init__(self, safe_str: str) -> None:
        self.safe_str = safe_str

    def __hash__(self) -> int:
        return hash(f"SafeString__{self.safe_str}")

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SafeString) and other.safe_str == self.safe_str

    def __repr__(self) -> str:
        return f"SafeString(safe_str='{self.safe_str}')"


Node = Union[
    str,
    SafeString,
    "Tag",
    "TagTuple",
    list["Node"],
    Generator["Node", None, None],
]

TagTuple = tuple[str, tuple[Node, ...], str]


class Tag:
    def __init__(self, name: str, self_closing: bool = False) -> None:
        self.tag_start = f"<{name}"
        self.tag_start_no_attrs = f"{self.tag_start}>"
        self.closing_tag = f"</{name}>"
        if self_closing:
            self.no_children_close = "/>"
        else:
            self.no_children_close = f">{self.closing_tag}"
        self.rendered = f"{self.tag_start}{self.no_children_close}"

    def __call__(
        self,
        attributes: dict[SafeString | str, str | SafeString | None],
        *children: Node,
    ) -> Union[TagTuple, SafeString]:
        if attributes:
            # in this case this is faster than attrs = "".join([...])
            attrs = ""
            val: str | SafeString | None
            for key, val in attributes.items():
                # optimization: a large portion of attribute keys should be
                # covered by this check. It allows us to skip escaping
                # where it is not needed. Note this is for attribute names only;
                # attributes values are always escaped (when they are `str`s)
                if key not in _common_safe_attribute_names:
                    key = (
                        escape_attribute_key(key)
                        if isinstance(key, str)
                        else key.safe_str
                    )

                if isinstance(val, str):
                    attrs += f' {key}="{faster_escape(val)}"'
                elif isinstance(val, SafeString):
                    attrs += f' {key}="{val.safe_str}"'
                elif val is None:
                    attrs += f" {key}"

            if children:
                return f"{self.tag_start}{attrs}>", children, self.closing_tag
            else:
                return SafeString(f"{self.tag_start}{attrs}{self.no_children_close}")
        elif children:
            return self.tag_start_no_attrs, children, self.closing_tag
        else:
            return SafeString(self.rendered)

