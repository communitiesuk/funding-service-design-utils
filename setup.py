# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

package_data = {"": ["*"]}

setup_kwargs = {
    "packages": find_packages(),
    "package_data": package_data,
}

setup(**setup_kwargs)
