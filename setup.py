#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='findmyhash',
    version='2.0-dev',
    description="Online hash finder",
    url="https://github.com/Talanor/findmyhash",
    maintainer="Quentin POIRIER",
    maintainer_email="talanor@talanor.fr",
    packages=[
        'findmyhash',
        'findmyhash.services'
    ],
    package_dir={
        "findmyhash": "./findmyhash",
        "findmyhash.services": "./findmyhash/services"
    },
    scripts=["./hash-tool.py"]
)