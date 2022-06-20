# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["fsd_tech"]

package_data = {"": ["*"]}

setup_kwargs = {
    "name": "fsd-tech",
    "version": "0.0.1",
    "description": "Utils for the fsd-tech team",
    "long_description": None,
    "author": "DLUHC",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "python_requires": ">=3.10,<4.0",
}


setup(**setup_kwargs)