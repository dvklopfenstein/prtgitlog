#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path as op

from glob import glob
from setuptools import setup
from setup_helper import SetupHelper


name = "prtgitlog"
classifiers = [
    'Programming Language :: Python',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Version Control :: Git',
    ]

# Use the helper
h = SetupHelper(initfile="src/prtgitlog/__init__.py", readmefile="README.md")

setup_dir = op.abspath(op.dirname(__file__))
requirements = ['wget'] + [x.strip() for x in
                           open(op.join(setup_dir, 'requirements.txt')).readlines()]

setup(
    name=name,
    version=h.version,
    author=h.author,
    author_email=h.email,
    license=h.license,
    long_description=h.long_description,
    packages=['prtgitlog',],
    package_dir={'prtgitlog': 'src/prtgitlog'},
    # packages=[name, name + ".test_data", name + ".anno"],
    # include_package_data=True,
    # package_data={"goatools.test_data.nbt_3102": ["*.*"]},
    scripts=glob('scripts/*.py'),
    classifiers=classifiers,
    url='http://github.com/dvklopfenstein/src/prtgitlog',
    description="'git log' history results reformatted and grouped by day to year",
    install_requires=requirements
)
