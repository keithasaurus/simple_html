import sys
import time
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
sys.path.append(str(Path(__file__).parent))

env = Environment(
    loader=PackageLoader("jinja_example"),
    autoescape=select_autoescape()
)
template = env.get_template("template.html")

# jinja2
time_start = time.time()
for i in range(20000):
    x = template.render(
        title="some title",
        content="some content",
        oks=["okokok" for _ in range(10)]
    )

print(time.time() - time_start, "seconds")
