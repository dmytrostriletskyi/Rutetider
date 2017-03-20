#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: DmytryiStriletskyi
@contact: dmytryi.striletskyi@gmail.com
@license: MIT License
Copyright (C) 2017
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='rutetider',
    version='1.0.0',
    author='DmytryiStriletskyi',
    author_email='dmytryi.striletskyi@gmail.com',
    url='https://github.com/DmytryiStriletskyi/rutetider',
    description='SQL-module for Rutetider',
    download_url='https://github.com/DmytryiStriletskyi/rutetider/archive/master.zip',
    license='MIT',

    packages=['rutetider (separate pypi)'],
    install_requires=['psycopg2'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
