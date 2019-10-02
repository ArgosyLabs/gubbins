#!/usr/bin/env python3
from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "gubbins",
    version = "0.0.1",
    description = ("Serial number generator/validator"),
    url = "https://github.com/ArgosyLabs/gubbins",
    author = "Derrick Lyndon Pallas",
    author_email = "derrick@argosylabs.com",
    license = "MIT",
    packages = [ "gubbins" ],
    install_requires = [ "more_itertools", "anybase32", "pynumparser" ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = "serial generator validator",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
)
#
