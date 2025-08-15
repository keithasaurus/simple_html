from setuptools import setup, find_packages
from mypyc.build import mypycify


setup(
    name="simple_html",
    ext_modules=mypycify([
        "simple_html/utils.py",
    ]),
    packages="simple_html",
    python_requires=">=3.9",
)
