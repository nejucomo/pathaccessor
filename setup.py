#!/usr/bin/env python

from setuptools import setup, find_packages


PACKAGE = 'accessorpath'

setup(
    name=PACKAGE,
    description='Track the attribute/index/key path into a dicts-and-lists data structure.',
    version='0.1',
    author='Nathan Wilcox',
    author_email='nejucomo+dev@gmail.com',
    license='GPLv3',
    url='https://github.com/nejucomo/{}'.format(PACKAGE),
    install_requires=[
    ],

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            '{} = {}.main:main'.format(
                PACKAGE.replace('_', '-'),
                PACKAGE,
            )
        ],
    }
)
