#!/usr/bin/env python
"""Add and remove markers for a file.

     2017_09_29 Fri
       Fri 2017-09-29 10:24:53 DV A Initial commit
       Fri 2017-09-29 10:26:39 99ccf46 B Add git log files.
       Fri 2017-09-29 10:28:09 a29b6c3 C Changed pkg name to prtgitlog
       Fri 2017-09-29 11:10:52 72bb16e D Put each class into its own module.
         A... A .gitignore
         .BC. A src/bin/gitlog.py
         .B.. M src/gitlog_prt/gitlog.py
         .B.. M src/gitlog_prt/cli.py
         ..CD A src/prtgitlog/gitlog.py
         ..C. A src/prtgitlog/cli.py
         ...D A src/prtgitlog/sortbytime.py
         ...D A src/prtgitlog/prthdrs.py
         ...D A src/prtgitlog/data.py
"""

__copyright__ = "Copyright (c) 2014-2018, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import sys
import prtgitlog.cli as cli
from prtgitlog.cli import DocoptParse


def test_one_file():
    """Add and remove markers for a file."""
    args_exp = [
    #    args       expected dict
    #    --------   ---------------------
        ([],        {'by_time': 'week'}),
        (['day'],   {'by_time': 'day'}),
        (['week'],  {'by_time': 'week'}),
        (['month'], {'by_time': 'month'}),
        (['year'],  {'by_time': 'year'}),
    ]
    doc = cli.__doc__
    for args, expected in args_exp:
        actual = DocoptParse(doc, args).get_dict()
        assert actual == expected, "ACT({}) != EXP({})".format(actual, expected)


if __name__ == '__main__':
    test_one_file()

# Copyright (c) 2014-2018, DV Klopfenstein. all rights reserved.
