#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""For installing prgitlog package and gitlog.py script."""


from distutils.core import setup
from setup_helper import SetupHelper


h = SetupHelper(initfile="src/prtgitlog/__init__.py", readmefile="README.md")

setup(
    name='prtgitlog',
    version=h.version,
    author=h.author,
    author_email=h.email,
    license=h.license,
    long_description=h.long_description,
    packages=['prtgitlog',],
    package_dir={'prtgitlog': 'src/prtgitlog'},
    scripts=['src/bin/gitlog.py'],
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
    description="'git log' history results reformatted and grouped by day to year",
    install_requires=['docopt'],
)
