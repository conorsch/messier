#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'blessings',
    'docopt',
    'python-vagrant',
    'pyyaml',
]
test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='messier',
    version='0.1.1',
    description="Test Ansible roles with Vagrant, similar to Test Kitchen",
    long_description=readme + '\n\n' + history,
    author="Conor Schaefer",
    author_email='conor.schaefer@gmail.com',
    url='https://github.com/conorsch/messier',
    packages=[
        'messier',
    ],
    package_dir={'messier':
                 'messier'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='messier',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    scripts=['bin/messier'],
    test_suite='tests',
    tests_require=test_requirements
)
