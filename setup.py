#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from setuptools import setup, find_packages
import tracking

setup(
    name='django-tracking-jl',
    version=tracking.get_version(),
    description="Basic visitor tracking and blacklisting for Django",
    long_description=open('README.rst', 'r').read(),
    keywords='django, tracking, visitors',
    author='Jaroslaw Lachowski',
    author_email='jalachowski@gmail.com',
    url='https://github.com/jlachowski/django-tracking',
    license='MIT',
    package_dir={'tracking': 'tracking'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ]
)
