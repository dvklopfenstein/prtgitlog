"""Print 'git log' headers for each time group."""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx


# pylint: disable=too-few-public-methods
class CommitFiles(object):
    """Print 'git log' headers for each time group."""

    def __init__(self, objalias, file2hash2stat):
        self.objalias = objalias
        self.ntdat, self.prtlet = self._get_data_letterstr(file2hash2stat)

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


# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
