"""Print 'git log' headers for each time group."""

__copyright__ = "Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx


# pylint: disable=too-few-public-methods
class CommitAliases(object):
    """Print 'git log' headers for each time group."""

    #      A-Z                   a-z                    0-9
    #      : ; < = > ? @         !"#$&"()+,-./        [ \ ] ^ _       { | } ~
    chrs = list(range(65, 91)) + list(range(97, 123)) + list(range(48, 58)) + \
           list(range(58, 65)) + list(range(33, 48)) + list(range(91, 96)) + \
           list(range(123, 127))

    def __init__(self, nts_cur):
        self.nthdrs = sorted(nts_cur, key=lambda nt: nt.datetime)
        self.ci2chr = self._init_ci2chr()

    def _init_ci2chr(self):
        """Initialize ci2chr (commit-hash -> alias)."""
        qty = len(self.chrs)
        ci_char = [(nt.commithash, chr(self.chrs[i%qty])) for i, nt in enumerate(self.nthdrs)]
        return cx.OrderedDict(ci_char)


# Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
