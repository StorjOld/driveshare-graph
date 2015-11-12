from setuptools import setup

setup(
    name ='driveshare-graph', version ='1.0',
    description = 'graph of Storj network activity',
    author = 'Andrew Kim', 
    url = 'http://storj.io',
    install_requires = ['flask','pymongo', 'pygal'],
    tests_require = ['coverage', 'coveralls'],
    test_suite = 'tests',
) 
