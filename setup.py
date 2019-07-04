# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains helpers for the DataLad handbook.
'''

requires = ['Sphinx']

setup(
    name='dataladhandbook',
    version='0.1',
    url='http://github.com/datalad-handbook/book',
    license='BSD',
    description='Various Sphinx-related helpers and types',
    long_description=long_desc,
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
