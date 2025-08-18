from typing import List, Tuple

from simple_html import (
    h1,
    html,
    title,
    head,
    body,
    div,
    p,
    ul,
    li,
    SafeString,
    br,
    meta,
    DOCTYPE_HTML5,
    render,
)


def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        render(h1("Hello, World!"))


def basic(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render(
            DOCTYPE_HTML5,
            html(
                head(title("A Great Web page!")),
                body(
                    h1({"class": "great header",
                        "id": "header1",
                        "other_attr": "5"},
                       "Welcome!"),
                    div(
                        p("What a great web page!!!", br, br),
                        ul([
                            li({"class": "item-stuff"}, SafeString(ss))
                            for ss in oks])))))


def basic_long(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render(
            DOCTYPE_HTML5,
            html(
                head(title(title_)),
                body(
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(

                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                ),
            ),
        )


def lorem_ipsum(titles: List[str]) -> None:
    for t in titles:
        render(
            html(
                {"lang": "en"},
                head(
                    meta({"charset": "UTF-8"}),
                    meta(
                        {
                            "name": "viewport",
                            "content": "width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0",
                        }
                    ),
                    meta({"http-equiv": "X-UA-Compatible", "content": "ie=edge"}),
                    title(t),
                ),
                body(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                ),
            )
        )
