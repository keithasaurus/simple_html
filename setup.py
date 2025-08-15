from setuptools import setup, find_packages
from mypyc.build import mypycify

ext_modules = mypycify([
    "simple_html/utils.py",
], opt_level="3")

print("HHHHEEEEUUUU!")
setup(
    name="simple_html",
    ext_modules=ext_modules,
    packages="simple_html",
    python_requires=">=3.9",
)
