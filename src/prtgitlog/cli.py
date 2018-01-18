"""Command-line interface for gitlog Python wrapper.

Usage:
  gitlog.py [options]
  gitlog.py [--day | --week | --month | --year | --all]
            [--re=PATTERN] [--re=PATTERN]
            [--after=AFTER]
            [--au | --noau]
            [--fullhash]
            [--sortby=<sortby>]
            [--noci=HASH] [--noci=HASH] [--noci=HASH,HASH]
            [--hdr=<date>]
  gitlog.py --help

Options:
  -h --help      Show this screen.

  --day          Group logs by day
  --week         Group logs by week
  --month        Group logs by month
  --year         Group logs by year
  --all          Print all logs ungrouped by time unit

  --au           Print author
  --noau         Do not print author

  --fullhash     Print full commit hash

  --re=PATTERN   Display only files which match the regex PATTERN (e.g. src/bin)
                 Multiple --re options are OR'd
  --after=AFTER      Only display git log items after the specified date
  --sortby=<sortby>  Sort files by commit alias or filename [default: alias]
  --noci=HASH        Do not print 'git log' information for specified commit hashes
  --hdr=<date>       Print header as one line per commit hash (default) or as commit date
"""

#  gitlog.py [--day | --week | --month | --year | --all]
#  gitlog.py [--re=PATTERN]
#  gitlog.py [options] [DAYS]
#  gitlog.py [DAYS] [options]
#  gitlog.py [--re=PATTERN]
#  gitlog.py [--re=PATTERN] --after=AFTER

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from docopt import docopt

def cli():
    """Command-line interface for gitlog Python wrapper."""
    obj = DocoptParse(__doc__, sys.argv[1:])
    return obj.docdct, obj.docclr, obj.get_dict(), obj.get_set(),  # _cli_kws()


class DocoptParse(object):
    """Put docopt dict in desired format."""

    # All keys from docopt used in gitlog
    kws_all = set(['--re', '--after',
                   '--au', '--noau',
                   '--fullhash',
                   '--day', '--week', '--month', '--year', '--all',
                   '--noci',
                   '--sortby',
                   '--hdr',
                   've',
                  ])
    # Values used "as is" from docopt
    kws_dct = set(['re'])
    # True/False values used "as is" from docopt.
    kws_set = set(['allhdrs', 'fullhash'])

    def __init__(self, doc, args):
        self.docdct = docopt(doc, args)
        # pylint: disable=line-too-long
        self.docclr = {k.replace('--', ''):v for k, v in self.docdct.items() if k in self.kws_all and v}

    def get_dict(self):
        """Simplify docopt keyword args."""
        # kws = {k:v for k, v in self.docdct.items() if k in self.kws_dict and v}
        kws = {k:v for k, v in self.docclr.items() if k in self.kws_dct}
        self.get_bytime(kws)
        self.get_after(kws)
        self.get_au(kws)
        self.get_noci(kws)
        self.get_sortby(kws)
        self.get_hdr_fmt(kws)
        return kws

    def get_set(self):
        """Get set kws."""
        return self.kws_set.intersection(self.docclr)  # TBD use au

    def get_after(self, kws):
        """Return 'after' key with appropriate time specified in value."""
        if 'after' in self.docclr:
            val = self.docclr['after']
            if val.isdigit():
                kws['after'] = '{N} days'.format(N=val)

    def get_bytime(self, kws):
        """Report gitlog by day, week(dflt), month, or year."""
        time_units = set(['--day', '--week', '--month', '--year', '--all'])
        bytime = [t for t in time_units if self.docdct[t]]
        kws['by_time'] = bytime[0][2:] if bytime else 'week'

    def get_au(self, kws):
        """User can override default settings for printing commit author name."""
        if 'au' in self.docclr:
            kws['au'] = True
        elif 'noau' in self.docclr:
            kws['au'] = False

    def get_noci(self, kws):
        """Add commit hashes that shall not be printed."""
        if 'noci' not in self.docclr:
            return
        noci_all = set()
        for noci_lst in self.docclr['noci']:
            noci_all.update(set(noci_lst.split(',')))
        kws['noci'] = noci_all

    def get_sortby(self, kws):
        """Sort file data for printing."""
        self._set_val(kws, 'sortby', set(['alias', 'filename']), 'alias')

    def get_hdr_fmt(self, kws):
        """User specified header format. Default is one line per commit hash."""
        if 'hdr' in self.docclr:
            self._set_val(kws, 'hdr', set(['date']), None)

    def _set_val(self, kws, key, exp_vals, val_dflt):
        """Sort file data for printing."""
        val_raw = self.docclr[key]
        val_set = exp_vals.intersection(set([val_raw]))
        assert len(val_set) <= 1
        if val_set:
            kws[key] = list(val_set)[0]
        # If user provided unrecognized value, use the default value
        elif val_dflt is not None:
            kws[key] = val_dflt


#### # TBD: docopt: --after --ve --allhdrs --noci
#### # pylint: disable=too-many-branches
#### def _cli_kws():
####     """Command-line interface for gitlog Python wrapper using a dict."""
####     #### kws = {'by_time':'week', 'after':'2016-01-12'}
####     kws = {'by_time':'week'}
####     re_exclude = [] # Do not report on any files matching these regexs
####     ci_exclude = set()
####     for arg in sys.argv[1:]:
####         if arg.isdigit():
####             kws['after'] = "{N} days".format(N=arg)
####         elif arg[:8] == '--after=':
####             valstr = arg[8:]
####             kws['after'] = None if valstr == "None" else valstr
####         elif arg[:5] == '--re=':              # DONE
####             kws['--re'] = arg[5:]             # DONE
####         elif arg[:3] == 've=':
####             kws['ve'] = re_exclude.append(arg[3:])
####         elif arg[:5] == 'noci=':
####             ci_str = arg[5:]
####             #int(ci_str, 16) # Throws error if digits are not hex
####             ci_exclude |= set(ci_str.split(',')) if ',' in ci_str else set([ci_str])
####         elif arg == "day":                    # DONE
####             kws['by_time'] = 'day'            # DONE
####         elif arg == "week":                   # DONE
####             kws['by_time'] = 'week'           # DONE
####         elif arg == "month":                  # DONE
####             kws['by_time'] = 'month'          # DONE
####         elif arg == "year":                   # DONE
####             kws['by_time'] = 'year'           # DONE
####         elif arg == "allhdrs":
####             kws['allhdrs'] = True
####     if re_exclude:
####         kws['ve'] = re_exclude
####     if ci_exclude:
####         kws['noci'] = ci_exclude
####     return kws

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
