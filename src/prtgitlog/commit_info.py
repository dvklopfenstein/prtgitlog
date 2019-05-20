"""Print 'git log' headers for each time group."""

__copyright__ = "Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import re


class CommitInfo(object):
    """Print 'git log' headers for each time group."""

    kws_dct = set(['au', 'hdr'])
    kws_set = set(['fullhash'])
    day2c = {'Mon':'M', 'Tue':'T', 'Wed':'W', 'Thu':'R', 'Fri':'F', 'Sat':'S', 'Sun':'U'}

    def __init__(self, objalias, **kws):
        self.kws = {k:v for k, v in kws.items() if k in self.kws_dct}
        self.objalias = objalias

    def prt_hdrs(self, hdrpat, prt):
        """Print headers."""
        # Use verbose header format (default)
        if 'hdr' not in self.kws:
            self._prt_verbose(prt, hdrpat)
        elif self.kws['hdr'] == 'date':
            # self._prt_date(prt, '%Y %b %d %a')  # 2018 Jan 01 Mon
            self._prt_date(prt, '%Y %b %d %w')  # 2018 Jan 01 1

    def num_commits(self):
        """Get the number of commits in this time unit"""
        return len(self.objalias.nthdrs)

    def _prt_verbose(self, prt, hdrpat):
        """Print headers with one line per commit."""
        # Ex: Sun 2018-01-14 23:51:49 c5a9255 T Added stats table
        for nthdr in self.objalias.nthdrs:
            ciletter = self.objalias.ci2chr[nthdr.commithash]
            # if ciletter in self.objalias.prtlet:
            # print('COMMIT LETTER({})'.format(ciletter))
            # print('NT HDR:', nthdr)
            prt.write(hdrpat.format(**self._get_patdict(nthdr, ciletter)))

    def _prt_date(self, prt, fmt='%Y %b %d %a'):
        """Print headers with one line per commit."""
        dates_str = self.getstr_dates(fmt)
        dates_trn = zip(*dates_str)
        if fmt[-2:] == "%w":
            weekdays = list(dates_trn[-1])
            weekdays.append(" -> 0=Sunday ... 6=Saturday")
            dates_trn[-1] = weekdays
        for elem in dates_trn:
            prt.write("    {DATES}\n".format(DATES="".join(elem)))

    def getstr_dates(self, fmt):
        """Return the commit dates as a string formatted as user-specified."""
        dates_str = []
        days = r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
        for nthdr in self.objalias.nthdrs:
            datestr = nthdr.datetime.strftime(fmt)
            if fmt[-2:] == "%a":
                datestr = re.sub(days, lambda m: self.day2c[m.group(1)], datestr)
            dates_str.append(datestr)
        return dates_str

    @staticmethod
    def _get_patdict(nthdr, ciletter):
        """Return a dict containing the commit letter and the key-vals in nthdr."""
        patdict = {k:v for k, v in nthdr._asdict().items()}
        patdict['abc'] = ciletter
        return patdict


# Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
