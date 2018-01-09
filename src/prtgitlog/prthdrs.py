"""Print 'git log' headers for each time group."""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx

class PrtHdrs(object):
    """Print 'git log' headers for each time group."""

    #      A-Z             a-z              0-9
    chrs = range(65, 91) + range(97, 123) + range(48, 58) + \
           range(58, 65) + range(33,48) + range(91, 96) + range(123, 127)
    #      : ; < = > ? @   !"#$&"()+,-./  [ \ ] ^ _       { | } ~

    def __init__(self, nts_cur, file2hash2stat):
        self.nthdrs = sorted(nts_cur, key=lambda nt: nt.datetime)
        _qty = len(self.chrs)
        #_ci_char = [(nt.commithash, chr(i+65)) for i, nt in enumerate(self.nthdrs)]
        _ci_char = [(nt.commithash, chr(self.chrs[i%_qty])) for i, nt in enumerate(self.nthdrs)]
        self.ci2chr = cx.OrderedDict(_ci_char)
        self.ntdat, self.prtlet = self._get_data_letterstr(file2hash2stat, self.ci2chr)

    def prt_hdrs(self, hdrpat, prt):
        """Print headers."""
        for nthdr in self.nthdrs:
            ciletter = self.ci2chr[nthdr.commithash]
            if ciletter in self.prtlet:
                prt.write(hdrpat.format(**self.get_patdict(nthdr, ciletter)))

    @staticmethod
    def get_patdict(nthdr, ciletter): # TBD: make private after adding another public method
        """Return a dict containing the commit letter and the key-vals in nthdr."""
        patdict = {k:v for k, v in nthdr._asdict().items()}
        patdict['abc'] = ciletter
        return patdict

    @staticmethod
    def _get_data_letterstr(file2hash2stat, ci2chr):
        """Get list of files, each with its checkins represented by an ASCII art letter string."""
        ntobj = cx.namedtuple("NtDataLet", "letterstr status filename")
        ret = []
        prtlet = set()
        if file2hash2stat is not None:
            for data, hash2stat in file2hash2stat.items():
                # ci2chr:  OrderedDict([('4c433a5', 'A'), ('92301ba', 'B')])
                ci_lst = [let if ci in hash2stat else "." for ci, let in ci2chr.items()]
                stats = [hash2stat[h][0] for h in ci2chr.keys() if h in hash2stat]
                prtlet |= set(ci_lst)
                ret.append(ntobj(letterstr="".join(ci_lst), status="".join(stats), filename=data))
        return ret, prtlet

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
