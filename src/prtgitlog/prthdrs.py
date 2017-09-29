"""Print 'git log' headers."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx

class PrtHdrs(object):
    """Print 'git log' headers."""

    def __init__(self, nts_cur, file2hashes):
        self.nthdrs = sorted(nts_cur, key=lambda nt: nt.datetime)
        self.ci2chr = cx.OrderedDict([(nt.commithash, chr(i+65)) for i, nt in enumerate(self.nthdrs)])
        self.ntdat, self.prtlet = self._get_data_letterstr(file2hashes, self.ci2chr)

    def prt_hdrs(self, hdrpat, prt):
        """Print headers."""
        for nthdr in self.nthdrs:
            ciletter = self.ci2chr[nthdr.commithash]
            if ciletter in self.prtlet:
                prt.write(hdrpat.format(**self._get_patdict(nthdr, ciletter)))

    @staticmethod
    def _get_patdict(nthdr, ciletter):
        """Return a dict containing the commit letter and the key-vals in nthdr."""
        patdict = {k:v for k, v in nthdr._asdict().items()}
        patdict['abc'] = ciletter
        return patdict

    @staticmethod
    def _get_data_letterstr(filename2checksums, ci2chr):
        """Return list of files, each with its checkins represented by an ASCII art letter string."""
        ntobj = cx.namedtuple("NtDataLet", "letterstr filename")
        ret = []
        prtlet = set()
        if filename2checksums is not None:
            for data, chkin_ids in filename2checksums.items():
                # ci2chr:  OrderedDict([('4c433a5', 'A'), ('92301ba', 'B')])
                ci_lst = [let if ci in chkin_ids else "." for ci, let in ci2chr.items()]
                prtlet |= set(ci_lst)
                ret.append(ntobj(letterstr="".join(ci_lst), filename=data))
        return ret, prtlet

# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
