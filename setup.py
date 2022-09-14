# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

package_data = {"": ["*"]}

install_requires = [
    "Flask-Babel>=2.0.0,<3.0.0",
    "PyYAML>=6.0,<7.0",
    "python-dotenv>=0.20.0,<0.21.0",
    "rich>=12.4.4,<13.0.0",
    "Flask>=2.1.1,<3.0.0",
    "python-json-logger>=2.0.2,<3.0.0",
    "gunicorn>=20.1.0,<21.0.0",
    "pytz>=2022.1",
    "PyJWT[crypto]>=2.4.0",
]

setup_kwargs = {
    "packages": find_packages(),
    "package_data": package_data,
    "install_requires": install_requires,
}

setup(**setup_kwargs)
