import time

from simple_html import title, html, head, body, div, h1, br
from simple_html.utils import templatize, render, Node


def html_func(name: str, age: int) -> Node:
    return html(
        head(title("hi, ", name)),
        body(
            div({"class": "content",
                 "blabla": "bla"},
                h1("hi ", name, "I'm ", age),
                br)
        )
    )

templatized = templatize(html_func)

# Example usage
if __name__ == "__main__":
    # result =
    # print(f"Type: {type(result)}")
    # print(f"Parts: {len(result)}")
    # print(f"Content: [{','.join(str(part) for part in result)}]")
    start_1 = time.time()
    for _ in range(10000):
        render(html_func(name="Hello' World", age=300))
    end_1 = time.time() - start_1
    print(end_1)

    print(render(html_func(name="Hello' World", age=300)))

    start_2 = time.time()
    for _ in range(10000):
        render(templatized(name="Hello' World", age=300))
    end_2 = time.time() - start_2
    print(end_2)

    print(render(templatized(name="Hello' World", age=300)))