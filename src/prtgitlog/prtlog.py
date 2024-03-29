"""Return data from 'git log' organized by coarse time unit."""

__copyright__ = "Copyright (C) 2017-present, DV Klopfenstein, PhD. All rights reserved."
__author__ = "DV Klopfenstein, PhD"

from prtgitlog.commit_aliases import CommitAliases
from prtgitlog.commit_info import CommitInfo
from prtgitlog.commit_files import CommitFiles

# pylint: disable=too-few-public-methods
class PrtLog:
    """Return data from 'git log' organized by coarse time unit."""

    kws_dct = {'au', 'sortby', 'hdr', 'by_time'}

    dflt_pat = {
        # Section header. Sections are by day, week, or month
        'section': "\n{TIMEUNIT} STARTING ON: {DATE} {Mon} - {C} commits, {F} files\n",
        'hdr_au': "  {weekday} {datetime} {chash} {abc} {author} {hdr}\n",
        'hdr': "  {weekday} {datetime} {chash:7} {abc} {hdr}\n",
        'dat': "    {CIs} {STATUS:>2} {DATA}\n"
    }

    def __init__(self, objtimesort, kws, fullhash):
        self.objtimesort = objtimesort
        self.kws = {k:v for k, v in kws.items() if k in self.kws_dct}
        self.fmt = {
            'sec': self.dflt_pat['section'],
            'hdr': self._init_hdr(fullhash),
            'dat': self.dflt_pat['dat'],
        }

    def prt_time2gitlog(self, prt):
        """Print 'git log' data by any of day, week, month, etc."""
        for day, ntday in self.objtimesort.get_time2hdrsdata().items():
            if ntday.file2hashstat is not None:
                self._prt_timegroup(prt, day, ntday)

    def _prt_timegroup(self, prt, day, ntday):
        """Print header lines and filenames for one time group."""
        objalias = CommitAliases(ntday.nthdrs)  # , ntday.file2hashstat)
        objhdrs = CommitInfo(objalias, **self.kws)
        objfile = CommitFiles(objalias, ntday.file2hashstat, **self.kws)
        prt.write(self.fmt['sec'].format(
            TIMEUNIT=self.kws['by_time'].title(),
            Mon=day.strftime('%a'),
            DATE=day.strftime("%Y_%m_%d"),
            C=objhdrs.num_commits(),
            F=objfile.num_files()))
        objhdrs.prt_hdrs(self.fmt['hdr'], prt)
        objfile.prt_data(self.fmt['dat'], prt)

    def _init_hdr(self, fullhash):
        """Initialize print format for the git commit header text."""
        dat = self.dflt_pat['hdr' if len(self.objtimesort.get_authors()) <= 2 else 'hdr_au']
        if 'au' in self.kws:
            dat = self.dflt_pat['hdr_au'] if self.kws['au'] else self.dflt_pat['hdr']
        if fullhash:
            dat = dat.replace('chash', 'commithash')
        return dat

# Copyright (C) 2017-present, DV Klopfenstein, PhD. All rights reserved.
