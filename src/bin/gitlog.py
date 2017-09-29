#!/usr/bin/env python
"""Run 'git log', printing results rearranged for easier reading."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import sys
from gitlog_prt.cli import cli
from gitlog_prt.gitlog import GitLog

def main():
  """Run 'git log', printing results rearranged for easier reading."""
  kws = cli()
  obj = GitLog(**kws)
  by_time = kws.get('by_time', 'by_day')
  obj.run(by_time, sys.stdout)
  #print(kws)

if __name__ == '__main__':
  main()

# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
