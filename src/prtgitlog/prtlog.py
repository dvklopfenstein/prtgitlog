"""Return data from 'git log' organized by coarse time unit."""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import re
from prtgitlog.commit_aliases import CommitAliases

# pylint: disable=too-few-public-methods
class PrtLog(object):
    """Return data from 'git log' organized by coarse time unit."""

    kws_dct = set(['au', 'sortby', 'hdrs'])
    kws_set = set(['fullhash'])

    dflt_pat = {
        'section': "\n{DATE} {Mon}\n", # Section header. Sections are by day, week, or month
        'hdr_au': "  {weekday} {datetime} {chash} {abc} {author} {hdr}\n",
        'hdr': "  {weekday} {datetime} {chash:7} {abc} {hdr}\n",
        'dat': "    {CIs} {STATUS:>2} {DATA}\n"
    }

    def __init__(self, objtimesort, kws, keys):
        self.objtimesort = objtimesort
        self.kws = {k:v for k, v in kws.items() if k in self.kws_dct}
        self.keys = keys.intersection(self.kws_set)
        self.fmt = {
            'sec': self.dflt_pat['section'],
            'hdr': self._init_hdr(),
            'dat': self.dflt_pat['dat'],
        }
        self.sorted = {
            'alias': self.sorted_alias,
            'filename': self.sorted_filename,
        }
        # self.max_letstr = 100

    def prt_time2gitlog(self, prt):
        """Print 'git log' data by any of day, week, month, etc."""
        for day, ntday in self.objtimesort.get_time2hdrsdata().items():
            if ntday.file2hashstat is not None:
                self._prt_timegroup(prt, day, ntday)

    def _prt_timegroup(self, prt, day, ntday):
        """Print header lines and filenames for one time group."""
        prt.write(self.fmt['sec'].format(Mon=day.strftime('%a'), DATE=day.strftime("%Y_%m_%d")))
        objhdr = self._prt_hdrs(prt, ntday.nthdrs, ntday.file2hashstat)
        data_sorted = self.sorted[self.kws['sortby']](objhdr.ntdat)
        fmtdat = self.fmt['dat']
        for ntd in data_sorted:
            #print("FFFFFFFFFFFFFFF", ntd.filename)
            status = re.sub(r'([A-Z])\1+', r'\1', ntd.status)  # rm duplicate Ms ...
            letstr = self._get_letstr(ntd.letterstr)
            prt.write(fmtdat.format(CIs=letstr, STATUS=status, DATA=ntd.filename))

    def _prt_hdrs(self, prt, nthdrs, file2hashstat):
        """Print header lines for one time group."""
        objhdr = CommitAliases(nthdrs, file2hashstat)
        objhdr.prt_hdrs(self.fmt['hdr'], prt)
        # CommitAliases creates filename letter strings
        return objhdr

    @staticmethod
    def sorted_alias(ntdata):
        """Sort files listed in 'git log'."""
        return sorted(ntdata, key=lambda nt: [nt.letterstr, nt.filename], reverse=True)

    @staticmethod
    def sorted_filename(ntdata):
        """Sort files listed in 'git log'."""
        return sorted(ntdata, key=lambda nt: [nt.filename, nt.letterstr], reverse=False)

    @staticmethod
    def _get_letstr(letterstr):
        """Get letterstr for printing."""
        # if len(letterstr) > self.max_letstr:
        #     return letterstr.replace('.', '')
        return letterstr

    def _init_hdr(self):
        """Initialize print format for the git commit header text."""
        dat = self.dflt_pat['hdr'] if len(self.objtimesort.get_authors()) <= 2 else ['hdr_au']
        if 'au' in self.kws:
            dat = self.dflt_pat['hdr_au'] if self.kws['au'] else self.dflt_pat['hdr']
        if 'fullhash' in self.keys:
            dat = dat.replace('chash', 'commithash')
        return dat


# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
