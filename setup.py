#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import setup, find_packages

import os
import setuptools


# Fix for debian 7 python that raise error on at_exit at the end of setup.py
# (cf http://bugs.python.org/issue15881)
try:
    import multiprocessing
except ImportError:
    pass

# Better to use exec to load the VERSION so to not have to import the alignak package:
with open(os.path.join('alignak_module_example', 'version.py')) as fh:
    ns = {}
    exec(fh.read(), ns)
    VERSION = ns['VERSION']


os.environ['PBR_VERSION'] = VERSION

setuptools.setup(
    setup_requires=['pbr'],
    version=VERSION,
    pbr=True,
)
