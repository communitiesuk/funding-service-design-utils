# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

package_data = {"": ["*"]}

install_requires = [
    "PyYAML>=6.0,<7.0",
    "python-dotenv>=0.20.0,<0.21.0",
    "rich>=12.4.4,<13.0.0",
    "Flask==2.0.2",
    "python-json-logger==2.0.2",
]

setup_kwargs = {
    "name": "funding-service-design-utils",
    "version": "0.0.8",
    "description": "Utils for the fsd-tech team",
    "long_description": None,
    "author": "DHULC",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "packages": find_packages(),
    "url": "https://github.com/communitiesuk/funding-service-design-utils",
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<4.0",
}

setup(**setup_kwargs)
