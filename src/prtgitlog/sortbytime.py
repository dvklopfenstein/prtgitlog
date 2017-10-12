"""Return data from 'git log' organized by coarse time unit."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx

class GitLogByTime(object):
    """Return data from 'git log' organized by coarse time unit."""

    def __init__(self, nts, timefnc):
        self.nts = nts
        self.timefnc = timefnc
        # Initialize
        self.time2file2hashes = None
        self.time2nts = None
        self._get_time2file2hashes()

    def get_time2hdrsdata(self):
        """For one time unit, return headers list and files list."""
        time_gitlog = []
        ntobj = cx.namedtuple("ntgitlog", "nthdrs file2hashes")
        hash2nt_all = {nt.commithash:nt for nt in self.nts}
        for time_cur, file2hashes in sorted(self.time2file2hashes.items()):
            #print "FFFFFF", file2hashes
            nts_cur = [hash2nt_all[h] for h in self.get_hashes(file2hashes.values())]
            nthdrs = sorted(nts_cur, key=lambda nt: nt.datetime)
            ntcur = ntobj(nthdrs=nthdrs, file2hashes=file2hashes)
            time_gitlog.append((time_cur, ntcur))
        #time_gitlog = [(t, ntobj(nthdrs=nthdrs[t], data=time2items.get(t, None))) for t in times]
        return cx.OrderedDict(time_gitlog)

    @staticmethod
    def get_hashes(commithashes): # TBD: make private after adding another public method
        """Get all commit hashes for all filenames in the set."""
        hashes_all = set()
        for hashes_cur in commithashes:
            hashes_all |= hashes_cur
        return hashes_all

    @staticmethod
    def _get_data_dictby(data):
        """Convert cx.defaultdict(lambda: cx.defaultdict(list)) to regular dicts."""
        day2data = {day:{} for day in data.keys()}
        for day, filename2commithash in data.items():
            for filename, commithash in filename2commithash.items():
                day2data[day][filename] = commithash
        return day2data

    def _get_time2file2hashes(self):
        """Return 'git log' data organized by day, week, etc..."""
        data = cx.defaultdict(lambda: cx.defaultdict(set))
        time2nts = cx.defaultdict(list)
        for ntd in self.nts:
            coarse_dt = self.timefnc(ntd.datetime)
            # print "TTTTTTTTTTTTT ({}) ({}) {}".format(ntd.datetime, coarse_dt, repr(ntd.datetime))
            chkin = ntd.commithash
            time2nts[coarse_dt].append(ntd)
            for filename in ntd.files:
                data[coarse_dt][filename].add(chkin)
        self.time2file2hashes = self._get_data_dictby(data)
        self.time2nts = {t:hs for t, hs in time2nts.items()}

# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
