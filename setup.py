#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""For installing prgitlog package and gitlog.py script."""

from distutils.core import setup


def _get_version():
    """Get the package's version from without using an import."""
    with open("src/prtgitlog/__init__.py", "r") as ifstrm:
        for line in ifstrm:
            if line[:15] == '__version__ = "':
                return line.rstrip()[15:-1]

setup(
    name='prtgitlog',
    version=_get_version(),
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    long_description=('A script to print "git log" output '
                      'in a concise and informative format\n\n'
                      'https://github.com/dvklopfenstein/'
                      'prtgitlog/blob/master/README.md'),
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
    install_requires=['docopt'],
)
