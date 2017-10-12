"""Command-line interface for gitlog Python wrapper."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


import sys


# TBD: Checkout docopt
def cli():
    """Command-line interface for gitlog Python wrapper."""
    kws = {}
    re_exclude = [] # Do not report on any files matching these regexs
    ci_exclude = set()
    for arg in sys.argv[1:]:
        if arg.isdigit():
            kws['after'] = "{N} days".format(N=arg)
        elif arg[:3] == 're=':
            kws['re'] = arg[3:]
        elif arg[:3] == 've=':
            kws['ve'] = re_exclude.append(arg[3:])
        elif arg[:5] == 'noci=':
            ci_str = arg[5:]
            #int(ci_str, 16) # Throws error if digits are not hex
            ci_exclude |= set(ci_str.split(',')) if ',' in ci_str else set([ci_str])
        elif arg == "byweek":
            kws['by_time'] = 'by_week'
        elif arg == "bymon":
            kws['by_time'] = 'by_month'
        elif arg == "allhdrs":
            kws['allhdrs'] = True
    kws['ve'] = re_exclude if re_exclude else None
    kws['noci'] = ci_exclude if ci_exclude else None
    return kws

# Copyright (c) 2014-2017, DV Klopfenstein. All rights reserved.
