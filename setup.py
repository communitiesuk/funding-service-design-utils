# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["fsd_tech"]

package_data = {"": ["*"]}

install_requires = [
    "Flask==2.0.2",
    "python-json-logger==2.0.2",
]

setup_kwargs = {
    "name": "fsd-tech",
    "version": "0.2.0",
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