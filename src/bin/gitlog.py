#!/usr/bin/env python
""" %prog [options]

  Run 'git log'. Then print results rearranged for easier reading.

    %prog --help

  Display this help message and exit.
"""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import sys
import re
from prtgitlog.cli import cli
from prtgitlog.gitlog import GitLog

def run_gitlog():
    """Run 'git log', printing results rearranged for easier reading."""
    kws = cli()
    obj = GitLog(**kws)
    by_time = kws.get('by_time', 'by_day')
    obj.run(by_time, sys.stdout)

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run_gitlog())

# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
