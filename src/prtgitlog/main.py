"""'git log' organized by day, week, or month."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2017-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import re
from prtgitlog.cli import cli
from prtgitlog.gitlog import GitLog
from argparse import ArgumentParser


def main(prt=True):
    """Run 'git log', printing results rearranged for easier reading."""
    doc, docc, kws, keys = cli()  # _ = ows
    args = None
    args = _get_args()
    if prt:
        print(f"DOC({doc})")
        print(f"CLR({docc})")
        print(f"KWS({kws})")
        print(f"KEYS({keys})")
    obj = GitLog(kws, keys)
    print(f'ARGS: {args}')
    # obj.prttxt_cmds(sys.stdout)
    obj.run(kws.get('by_time'), args.fullhash, sys.stdout)
    print(f'ARGS: {args}')
    print(f'BYTIME: {kws.get("by_time")}')
    if prt:
        print(f"DOC({doc})")
        print(f"CLR({docc})")
        print(f"KWS({kws})")
        print(f"KEYS({keys})")



def _get_args():
    parser = get_argparser()
    ##args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    print(f'ARGS: {args}')
    return args

def get_argparser():
    """Argument parser for Python wrapper of 'git log'"""
    parser = ArgumentParser(
        prog='gitlog',
        description='Concise "git log" for each affected file',
        add_help=True)
    parser.add_argument('filename')
    parser.add_argument('-g', '--group', choices=['day', 'week', 'year', 'all'])
    parser.add_argument('--au', action='store_false')
    parser.add_argument('--fullhash', action='store_true')
    # Date
    parser.add_argument('--since', )  #action='store_true')
    parser.add_argument('--after', )  #action='store_true')
    parser.add_argument('--until', )  #action='store_true')
    parser.add_argument('--before',)  # action='store_true')
    return parser

if __name__ == '__main__':
    main()

# Copyright (C) 2017-present, DV Klopfenstein. All rights reserved.
