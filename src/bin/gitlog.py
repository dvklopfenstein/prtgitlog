#!/usr/bin/env python
"""'git log' organized by day, week, or month."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import re
from prtgitlog.cli import cli
from prtgitlog.gitlog import GitLog


def run_gitlog():
    """Run 'git log', printing results rearranged for easier reading."""
    doc, opts, kws = cli()
    print("KWS({KWS})".format(KWS=kws))
    print("DOC({KWS})".format(KWS=doc))
    print("OPTS({KWS})".format(KWS=opts))
    obj = GitLog(**kws)
    obj.run(kws['by_time'], sys.stdout)
    print("KWS({KWS})".format(KWS=kws))
    print("DOC({KWS})".format(KWS=doc))
    print("OPTS({KWS})".format(KWS=opts))


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run_gitlog())

# Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved.
