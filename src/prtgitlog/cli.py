"""Print 'git log' output in a concise informative format

Usage:
  gitlog.py [FILE ...]
            [--day | --week | --month | --year | --all]
            [--re=PATTERN] [--re=PATTERN]
            [--au | --noau]
            [--fullhash]
            [--sortby=<sortby>]
            [--noci=HASH] [--noci=HASH] [--noci=HASH,HASH]
            [--hdr=<date>]
            [--since=DATE] [--after=DATE] [--until=DATE] [--before=DATE]
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

  --re=PATTERN   Display only files which match the regex PATTERN
                 (e.g. --re=src/bin)
                 Multiple --re options are OR'd

  --sortby=<sortby>  Sort files by commit property:
                     sortby=[alias|filename] [default: alias]
  --noci=HASH        Do not print 'git log' information for
                     specified commit hashes
  --hdr=<desc>       One descriptive line per commit (default) OR
                       a succinct date; desc=[date]

  --since=DATE   Display git log items more recent than the specified date
  --after=DATE   Display git log items more recent than the specified date
  --until=DATE   Display git log items older than the specified date
  --before=DATE  Display git log items older than the specified date

  --max-count=<number>  limit the number of commits to output

"""

#  gitlog.py [--day | --week | --month | --year | --all]
#  gitlog.py [--re=PATTERN]
#  gitlog.py [options] [DAYS]
#  gitlog.py [DAYS] [options]
#  gitlog.py [--re=PATTERN]
#  gitlog.py [--re=PATTERN] --after=AFTER

__copyright__ = "Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from docopt import docopt

def cli():
    """Command-line interface for gitlog Python wrapper."""
    obj = DocoptParse(__doc__, sys.argv[1:])
    return obj.docdct, obj.docclr, obj.get_dict(), obj.get_set(),  # _cli_kws()


# pylint: disable=line-too-long
class DocoptParse(object):
    """Put docopt dict in desired format."""

    # All keys from docopt used in gitlog
    kws_all = set(['--re',
                   '--au', '--noau',
                   '--fullhash',
                   '--day', '--week', '--month', '--year', '--all',
                   '--noci',
                   '--sortby',
                   '--hdr',
                   've',
                   # 'git log' options that are passed to the 'git log' command
                   '--after', '--since',   # Show commits more recent than a specific date
                   '--until', '--before',  # Show commits older than a specific date
                   '--max-count',
                  ])
    # Values used "as is" from docopt
    kws_dct = set(['re'])
    # True/False values used "as is" from docopt.
    kws_set = set(['allhdrs', 'fullhash'])

    def __init__(self, doc, args):
        self.docdct = docopt(doc, args)
        ## print('DOCOPT:', self.docdct)
        # pylint: disable=line-too-long
        self.docclr = {k.replace('--', ''):v for k, v in self.docdct.items() if k in self.kws_all and v}

    def get_dict(self):
        """Simplify docopt keyword args."""
        # kws = {k:v for k, v in self.docdct.items() if k in self.kws_dict and v}
        kws = {k:v for k, v in self.docclr.items() if k in self.kws_dct}
        ## print('CLI KWS:', kws)
        self.get_files(kws)
        self.get_bytime(kws)
        self.get_date(kws)  # --after --since --until --before
        self.get_au(kws)
        self.get_noci(kws)
        self.get_sortby(kws)
        self.get_hdr_fmt(kws)
        ## print('CLI KWS:', kws)
        return kws

    def get_files(self, kws):
        """Get files, if provided by user on command line"""
        fins = set()
        for fin in self.docdct['FILE']:
            if os.path.exists(fin):
                fins.add(fin)
            else:
                # pylint: disable=superfluous-parens
                print('  **WARNING FILE NOT FOUND: {F}'.format(F=fin))
        kws['files'] = fins
        if fins:
            # pylint: disable=superfluous-parens
            print('  Reporting on {N} user-specified files'.format(N=len(fins)))

    def get_set(self):
        """Get set kws."""
        return self.kws_set.intersection(self.docclr)  # TBD use au

    def get_date(self, kws):
        """Return 'after' key with appropriate time specified in value."""
        for key in set(['after', 'since', 'until', 'before']).intersection(self.docclr):
            val = self.docclr[key]
            if val.isdigit():
                kws[key] = '{N} days'.format(N=val)
            else:
                kws[key] = val

    def get_bytime(self, kws):
        """Report gitlog by day, week(dflt), month, or year."""
        time_units = set(['--day', '--week', '--month', '--year', '--all'])
        bytime = [t for t in time_units if self.docdct[t]]
        if bytime:
            kws['by_time'] = bytime[0][2:]

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


# Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
