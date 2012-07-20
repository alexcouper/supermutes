#!/usr/bin/env python
# # coding: utf-8

from setuptools import setup
long_description = open('README').read()


setup(
    name='supermutes',
    description='A collection of super mutables',
    long_description=long_description,
    version='0.1.7',
    author='Alex Couper',
    author_email='info@alexcouper.com',
    url='https://github.com/alexcouper/supermutes',
    packages=['supermutes'],
    zip_safe=True,
    package_data={
        '': ['*.txt', '*.rst'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
