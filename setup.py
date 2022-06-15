# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["fsd_tech"]

package_data = {"": ["*"]}

install_requires = [
    "PyYAML>=6.0,<7.0",
    "python-dotenv>=0.20.0,<0.21.0",
    "rich>=12.4.4,<13.0.0",
]

setup_kwargs = {
    "name": "fsd-tech",
    "version": "0.1.0",
    "description": "Utils for the fsd-tech team",
    "long_description": None,
    "author": "Version 1",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<4.0",
}


setup(**setup_kwargs)
