#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""For installing prgitlog package and gitlog.py script."""

from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import setup

def get_long_description():
    """Return the contents of the README.md as a string"""
    dir_cur = abspath(dirname(__file__))
    # python3
    #with open(join(dir_cur, 'README.md'), encoding='utf-8') as ifstrm:
    # python3 or python2
    with open(join(dir_cur, 'README.md'), 'rb') as ifstrm:
        return ifstrm.read().decode("UTF-8")

setup(
    name='prtgitlog',
    version='0.1.19',
    author='DV Klopfenstein',
    author_email='dvklopfenstein@protonmail.com',
    packages=['prtgitlog',],
    package_dir={'prtgitlog': 'src/prtgitlog'},
    scripts=['src/bin/gitlog'],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Version Control :: Git',
    ],
    url='http://github.com/dvklopfenstein/prtgitlog',
    description="A script to print 'git log' output in a concise informative format",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=['docopt'],
)

# Copyright 2017-present, DV Klopfenstein, PhD. All rights reserved.
