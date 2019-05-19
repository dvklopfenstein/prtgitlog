"""Print 'git log' headers for each time group."""

__copyright__ = "Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx
import re


class CommitFiles(object):
    """Print 'git log' headers for each time group."""

    kws_dct = set(['sortby'])
    # kws_set = set(['fullhash'])

    def __init__(self, objalias, file2hash2stat, **kws):
        self.kws = {k:v for k, v in kws.items() if k in self.kws_dct}
        self.objalias = objalias
        self.ntdat, self.prtlet = self._get_data_letterstr(file2hash2stat)
        self.sorted = {
            'alias': self._fnc_sorted_alias,
            'filename': self._fnc_sorted_filename,
        }
        # self.max_letstr = 100

    def prt_data(self, fmt, prt):
        """Print the list of files that have been commited."""
        data_sorted = self.sorted[self.kws['sortby']](self.ntdat)
        max_len_stat = max(len(set(nt.status)) for nt in self.ntdat)
        fmt = fmt.replace('2', str(max_len_stat))
        for ntd in data_sorted:
            #print("FFFFFFFFFFFFFFF", ntd.filename)
            status = re.sub(r'([A-Z])\1+', r'\1', ntd.status)  # rm duplicate Ms ...
            letstr = self._get_letstr(ntd.letterstr)
            prt.write(fmt.format(CIs=letstr, STATUS=status, DATA=ntd.filename))

    def num_files(self):
        """Get the number of files commited"""
        return len(self.sorted[self.kws['sortby']](self.ntdat))

    def _get_data_letterstr(self, file2hash2stat):
        """Get list of files, each with its checkins represented by an ASCII art letter string."""
        ntobj = cx.namedtuple("NtDataLet", "letterstr status filename")
        ret = []
        prtlet = set()
        ci2chr = self.objalias.ci2chr
        if file2hash2stat is not None:
            for data, hash2stat in file2hash2stat.items():
                # ci2chr:  OrderedDict([('4c433a5', 'A'), ('92301ba', 'B')])
                ci_lst = [let if ci in hash2stat else "." for ci, let in ci2chr.items()]
                stats = [hash2stat[h][0] for h in ci2chr.keys() if h in hash2stat]
                prtlet |= set(ci_lst)
                ret.append(ntobj(letterstr="".join(ci_lst), status="".join(stats), filename=data))
        return ret, prtlet

    @staticmethod
    def _fnc_sorted_alias(ntdata):
        """Sort files listed in 'git log'."""
        return sorted(ntdata, key=lambda nt: [nt.letterstr, nt.filename], reverse=True)

    @staticmethod
    def _fnc_sorted_filename(ntdata):
        """Sort files listed in 'git log'."""
        return sorted(ntdata, key=lambda nt: [nt.filename, nt.letterstr], reverse=False)

    @staticmethod
    def _get_letstr(letterstr):
        """Get letterstr for printing."""
        # if len(letterstr) > self.max_letstr:
        #     return letterstr.replace('.', '')
        return letterstr


# Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
