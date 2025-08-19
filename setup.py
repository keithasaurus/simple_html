from pathlib import Path

from setuptools import setup
from mypyc.build import mypycify

ext_modules = mypycify([
    "simple_html/utils.py",
])

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



setup(
    name="simple_html",
    ext_modules=ext_modules,
    author="Keith Philpott",
    packages=["simple_html"],
    python_requires=">=3.9",
    version="4.1.2",
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