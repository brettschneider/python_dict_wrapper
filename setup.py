#! /usr/bin/env python

from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name = 'python-dict-wrapper',
    py_modules = ['python_dict_wrapper'],
    version = '0.3',
    description = 'Wraps python dictionary keys are attributes',
    long_description=long_description,
    author = 'Steve Brettschneider',
    author_email = 'steve@bluehousefamily.com',
    url = 'https://github.com/brettschneider/python_dict_wrapper',
    download_url = 'https://github.com/brettschneider/python_lazy_streams/archive/0.2.tar.gz',
    keywords = ['dictionary', 'wrapper', 'attributes', 'enforce'],
    classifiers = []
)
