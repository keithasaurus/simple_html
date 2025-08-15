from setuptools import setup
from mypyc.build import mypycify

ext_modules = mypycify([
    "simple_html/utils.py",
])

setup(
    name="simple_html",
    ext_modules=ext_modules,
    packages=["simple_html"],
    python_requires=">=3.9",
)