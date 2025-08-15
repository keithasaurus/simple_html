from setuptools import setup, find_packages
from mypyc.build import mypycify


setup(
    name="simple-html",
    ext_modules=mypycify([
        "simple_html/utils.py",
    ]),
    packages=find_packages(),
    python_requires=">=3.9",
)
