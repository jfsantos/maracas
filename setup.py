# -*- coding: utf-8 -*-
# Copyright 2016 João Felipe Santos, jfsantos@emt.inrs.ca
#
# This file is part of the fuhai library, and is licensed under the
# MIT license.
from setuptools import setup, find_packages

setup(
    name = "fuhai",
    version = "0.0.1",
    packages = find_packages(),

    install_requires = [
        'numpy',
        'scipy',
    ],

    tests_require = [
      'nose'
    ],

    test_suite = 'nose.collector',

    entry_points = {
#        'console_scripts': [
#            'fuhai = fuhai.fuhai:main',
        ]
    }
)

