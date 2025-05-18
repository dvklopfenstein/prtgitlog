"""'git log' organized by day, week, or month."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2017-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import re
from prtgitlog.cli import get_cli
from prtgitlog.gitlog import GitLog
from argparse import ArgumentParser


def main(prt=True):
    """Run 'git log', printing results rearranged for easier reading."""
    cli, doc, docc, kws, keys = get_cli()  # _ = ows
    if prt:
        print(f"DOC({doc})")
        print(f"CLR({docc})")
        print(f"KWS({kws})")
        print(f"KEYS({keys})")
    obj = GitLog(cli.args, kws, keys)
    # obj.prttxt_cmds(sys.stdout)
    ####obj.run(kws.get('by_time'), args.fullhash, sys.stdout)
    obj.run(cli.args, cli.args.fullhash, sys.stdout)
    ####print(f'BYTIME: {kws.get("by_time")}')
    if prt:
        print(f"DOC({doc})")
        print(f"CLR({docc})")
        print(f"KWS({kws})")
        print(f"KEYS({keys})")


if __name__ == '__main__':
    main()

# Copyright (C) 2017-present, DV Klopfenstein. All rights reserved.
