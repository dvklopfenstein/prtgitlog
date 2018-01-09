"""Return data from 'git log' organized by coarse time unit."""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import re
from prtgitlog.prthdrs import PrtHdrs

# pylint: disable=too-few-public-methods
class PrtLog(object):
    """Return data from 'git log' organized by coarse time unit."""

    def __init__(self, objtimesort, prtpat):
        self.objtimesort = objtimesort
        self.sec = prtpat['section']
        self.hdr = self._init_hdr(prtpat)
        self.dat = prtpat['dat']

    def prt_time2gitlog(self, prt):
        """Print 'git log' data by any of day, week, month, etc."""
        for day, ntday in self.objtimesort.get_time2hdrsdata().items():
            if ntday.file2hashstat is not None:
                self._prt_timegroup(prt, day, ntday)

    def _prt_timegroup(self, prt, day, ntday):
        """Print header lines and filenames for one time group."""
        prt.write(self.sec.format(Mon=day.strftime('%a'), DATE=day.strftime("%Y_%m_%d")))
        objhdr = PrtHdrs(ntday.nthdrs, ntday.file2hashstat)
        objhdr.prt_hdrs(self.hdr, prt)
        for ntd in sorted(objhdr.ntdat, key=lambda n: [n.letterstr, n.filename], reverse=True):
            status = re.sub(r'([A-Z])\1+', r'\1', ntd.status)  # rm duplicate Ms ...
            prt.write(self.dat.format(CIs=ntd.letterstr, STATUS=status, DATA=ntd.filename))

    def _init_hdr(self, prtpat):
        """Initialize print format for the git commit header text."""
        return prtpat['hdr'] if len(self.objtimesort.get_authors()) <= 2 else prtpat['hdr_au']


# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
