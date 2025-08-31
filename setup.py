try:
    import tomllib
except ModuleNotFoundError:
    # python 3.10 and earlier
    import tomli as tomllib

from pathlib import Path
from setuptools import setup
from mypyc.build import mypycify

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open(this_directory / "pyproject.toml", "rb") as f:
    toml_data = tomllib.load(f)

project_data = toml_data["project"]

setup(
    name="simple-html",
    ext_modules=mypycify([
        "simple_html/core.py",
    ]),
    author=project_data["authors"][0]["name"],
    packages=["simple_html"],
    python_requires=project_data["requires-python"],
    version=project_data["version"],
    description=project_data["description"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license ="MIT",
    url=project_data["urls"]["Homepage"],
    classifiers = project_data["classifiers"],
    keywords=["html", "type hints"]
)