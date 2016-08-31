#!/usr/bin/env python

from distutils.core import setup

setup(
    name='cremi',
    version='0.7',
    description='Python Package for the CREMI Challenge',
    author='Jan Funke',
    author_email='jfunke@iri.upc.edu',
    url='http://github.com/funkey/cremi_python',
    packages=['cremi', 'cremi.io', 'cremi.evaluation'],
)
