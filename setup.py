#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import (
    setup,
    find_packages,
)
import versioneer

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 30.3.0']
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []

requires = [
    'Sphinx>=2',
    'sphinxcontrib-svg2pdfconverter',
    'sphinxcontrib-plantuml',
    'autorunrecord',
    'alabaster>=0.7.11',
]

if __name__ == '__main__':
    setup(name='dataladhandbook',
          version=versioneer.get_version(),
          cmdclass=versioneer.get_cmdclass(),
          setup_requires=SETUP_REQUIRES,
          packages=find_packages(),
          platforms='any',
          include_package_data=True,
          install_requires=requires,
          )
