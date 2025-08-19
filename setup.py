import tomllib
from pathlib import Path

from setuptools import setup
from mypyc.build import mypycify

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open(this_directory / "pyproject.toml", "rb") as f:
    pyproj_data = tomllib.load(f)

setup(
    name="simple-html",
    ext_modules=mypycify([
        "simple_html/utils.py",
    ]),
    author="Keith Philpott",
    packages=["simple_html"],
    python_requires=">=3.9",
    version=pyproj_data["version"],
    description="Template-less HTML rendering in Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/keithasaurus/simple_html",
    license = "MIT",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed'
    ],
    keywords=["html", "type hints"]
)