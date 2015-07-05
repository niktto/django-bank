#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import bank

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = bank.__version__
REQUIREMENTS = []


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()
elif sys.argv[-1] == 'develop':
    REQUIREMENTS = (
        open('requirements.txt').read().splitlines()
        + open('requirements-test.txt').read().splitlines()
    )
elif sys.argv[-1] == 'install':
    REQUIREMENTS = (
        open('requirements.txt').read().splitlines()
    )

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-bank',
    version=version,
    description="""Small Django app helping you to handle your users accounts""",
    long_description=readme + '\n\n' + history,
    author='Marek Szwalkiewicz',
    author_email='marek@szwalkiewicz.waw.pl',
    url='https://github.com/niktto/django-bank',
    packages=[
        'bank',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="BSD",
    zip_safe=False,
    keywords='django-bank',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
