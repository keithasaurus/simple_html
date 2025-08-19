import tomllib
from pathlib import Path

from setuptools import setup
from mypyc.build import mypycify

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open(this_directory / "pyproject.toml", "rb") as f:
    project_data = tomllib.load(f)["project"]

setup(
    name="simple-html",
    ext_modules=mypycify([
        "simple_html/utils.py",
    ]),
    author="Keith Philpott",
    packages=["simple_html"],
    python_requires=">=3.9",
    version=project_data["version"],
    description=project_data["description"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = project_data["license"],
    url=project_data["homepage"],
    classifiers = project_data["classifiers"],
    keywords=["html", "type hints"]
)