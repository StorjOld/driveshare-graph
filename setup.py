import os
from setuptools import setup

setup(
    name ='driveshare-graph', version ='1.0',
    description = 'graph of Storj network activity',
    author = 'Andrew Kim', 
    url = 'http://storj.io',
    install_requires = open("requirements.txt").readlines(),
    tests_require = open("test_requirements.txt").readlines(),
    test_suite = 'tests',
) 
