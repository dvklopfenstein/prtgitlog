#!/usr/bin/env python
"""'git log' organized by day, week, or month.

Usage:
  gitlog.py
  gitlog re=src

Options:
  -h --help     Show this screen.
  -b --by       (day|week|month|year)

"""

__copyright__ = "Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import re
from docopt import docopt
from prtgitlog.cli import cli
from prtgitlog.gitlog import GitLog

def run_gitlog():
    """Run 'git log', printing results rearranged for easier reading."""
    kws = cli()
    obj = GitLog(**kws)
    by_time = kws.get('by_time', 'by_week')
    obj.run(by_time, sys.stdout)
    arguments = docopt(__doc__, version='gitlog 0.10')
    print("ARGUMENTS({ARGS})".format(ARGS=arguments))

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run_gitlog())

# Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved.
