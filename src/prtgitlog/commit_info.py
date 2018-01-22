"""Print 'git log' headers for each time group."""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx


# pylint: disable=too-few-public-methods
class CommitInfo(object):
    """Print 'git log' headers for each time group."""

    def __init__(self, objalias):
        self.objalias = objalias

    def prt_hdrs(self, hdrpat, prt):
        """Print headers."""
        self._prt_verbose(prt, hdrpat)
        #self._prt_date(prt, '%Y %b %d')

    def _prt_verbose(self, prt, hdrpat):
        """Print headers with one line per commit."""
        for nthdr in self.objalias.nthdrs:
            ciletter = self.objalias.ci2chr[nthdr.commithash]
            # if ciletter in self.objalias.prtlet:
            prt.write(hdrpat.format(**self._get_patdict(nthdr, ciletter)))

    def _prt_date(self, prt, fmt='%Y %b %d'):
        """Print headers with one line per commit."""
        dates_str = [nthdr.datetime.strftime(fmt) for nthdr in self.nthdrs]
        dates_trn = zip(*dates_str)
        for date in dates_str:
            print("DDDDDDDDDDDDDDDDDDD", date)
        for elem in dates_trn:
            print("DDDDDDDDDDDDDDDDDDD", "".join(elem))

    @staticmethod
    def _get_patdict(nthdr, ciletter):
        """Return a dict containing the commit letter and the key-vals in nthdr."""
        patdict = {k:v for k, v in nthdr._asdict().items()}
        patdict['abc'] = ciletter
        return patdict


# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
