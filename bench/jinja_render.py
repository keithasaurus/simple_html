import time

from jinja2 import Environment, PackageLoader, select_autoescape

# todo: make this more equivalent to test of current code

env = Environment(
    loader=PackageLoader("jinja_example"),
    autoescape=select_autoescape()
)
template = env.get_template("template.html")

# jinja2
time_start = time.time()
for i in range(10000):
    x = template.render(title="some title", content="some content")

print(time.time() - time_start, "seconds")
