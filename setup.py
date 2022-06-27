# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["fsd_utils", "fsd_utils.config"]

package_data = {"": ["*"]}

install_requires = [
    "PyYAML>=6.0,<7.0",
    "python-dotenv>=0.20.0,<0.21.0",
    "rich>=12.4.4,<13.0.0",
]

setup_kwargs = {
    "name": "funding-service-design-utils",
    "version": "0.0.7",
    "description": "Utils for the fsd-tech team",
    "long_description": None,
    "author": "DHULC",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/communitiesuk/funding-service-design-utils",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<4.0",
}

setup(**setup_kwargs)
