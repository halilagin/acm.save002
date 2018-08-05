#!/usr/bin/env python

from setuptools import setup
import acm

setup(
    name='acm-ml-text-classification',
    version=str(acm.__version__),
    description='Acm text classification',
    author='Halil Agin',
    author_email='halil.agin@gmail.com',
    url='https://acm:8890/',
    packages=['acm', "acm/util", "acm/config", "acm/kafka"],
    install_requires=open('requirements.txt').read().split()
)
