"""Command-line interface for gitlog Python wrapper.

Usage:
  gitlog.py
  gitlog.py [options]
  gitlog.py [--re=PATTERN]
  gitlog.py [day|week|month|year]
  gitlog.py [DAYS]
  gitlog.py [DAYS] [day|week|month|year]
  gitlog.py [day|week|month|year] [DAYS]
  gitlog.py [--re=PATTERN] [day|week|month|year]
  gitlog.py [--re=PATTERN] [day|week|month|year] --after=AFTER

Options:
  -h --help      Show this screen.
  [day|week|month|year]  Display changes grouped by specified time increment
  DAYS           Only report all git logs after user-specified DAYS (integer)
  --re=PATTERN   Display only files which match the regex PATTERN (e.g. src/bin)
  --after=AFTER  Only display git log items after the specified date

"""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from docopt import docopt

def cli():
    """Command-line interface for gitlog Python wrapper."""
    obj = DocoptParse(__doc__, sys.argv[1:])
    return obj.docdct, obj.docclr, obj.get_dict(), _cli_kws()


class DocoptParse(object):
    """Put docopt dict in desired format."""

    kws_dict = set(['--re', 'DAYS', 've', 'noci'])
    kws_set = set(['allhdrs'])

    def __init__(self, doc, args):
        self.docdct = docopt(doc, args)
        self.docclr = {k:v for k, v in self.docdct.items() if k in self.kws_dict and v}

    def get_dict(self):
        """Simplify docopt keyword args."""
        # kws = {k:v for k, v in self.docdct.items() if k in self.kws_dict and v}
        kws = {}
        self.get_bytime(kws)
        self.get_after(kws)
        return kws

    def get_after(self, kws):
        """Return 'after' key with appropriate time specified in value."""
        keys = set(self.docclr.keys()).intersection(set(['DAYS', 'after']))
        if keys:
            assert len(keys) != 2, "CANNOT SPECIFY BOTH 'DAYS' AND --after"
            if 'DAYS' in keys:
                days = self.docclr['DAYS']
                assert days.isdigit(), "'DAYS' MUST BE AN INTEGER"
                kws['after'] = '{N} days'.format(N=days)

    def get_bytime(self, kws):
        """Report gitlog by day, week(dflt), month, or year."""
        bytime = [t for t in set(['day', 'week', 'month', 'year']) if self.docdct[t]]
        kws['by_time'] = bytime[0] if bytime else 'week'



# TBD: docopt: --after --ve --allhdrs --noci
# pylint: disable=too-many-branches
def _cli_kws():
    """Command-line interface for gitlog Python wrapper using a dict."""
    #### kws = {'by_time':'week', 'after':'2016-01-12'}
    kws = {'by_time':'week'}
    re_exclude = [] # Do not report on any files matching these regexs
    ci_exclude = set()
    for arg in sys.argv[1:]:
        if arg.isdigit():
            kws['after'] = "{N} days".format(N=arg)
        elif arg[:8] == '--after=':
            valstr = arg[8:]
            kws['after'] = None if valstr == "None" else valstr
        elif arg[:5] == '--re=':              # DONE
            kws['--re'] = arg[5:]             # DONE
        elif arg[:3] == 've=':
            kws['ve'] = re_exclude.append(arg[3:])
        elif arg[:5] == 'noci=':
            ci_str = arg[5:]
            #int(ci_str, 16) # Throws error if digits are not hex
            ci_exclude |= set(ci_str.split(',')) if ',' in ci_str else set([ci_str])
        elif arg == "day":                    # DONE
            kws['by_time'] = 'day'            # DONE
        elif arg == "week":                   # DONE
            kws['by_time'] = 'week'           # DONE
        elif arg == "month":                  # DONE
            kws['by_time'] = 'month'          # DONE
        elif arg == "year":                   # DONE
            kws['by_time'] = 'year'           # DONE
        elif arg == "allhdrs":
            kws['allhdrs'] = True
    if re_exclude:
        kws['ve'] = re_exclude
    if ci_exclude:
        kws['noci'] = ci_exclude
    return kws

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
