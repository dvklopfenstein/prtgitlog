"""Return data from 'git log' organized by coarse time unit."""

__copyright__ = "Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx


class GitLogByTime(object):
    """Return data from 'git log' organized by coarse time unit."""

    def __init__(self, nts, timefnc):
        self.nts = nts
        self.timefnc = timefnc
        # Initialize
        self.time2nts = None
        self.time2file2hashstat = None
        self._get_time2file2hashstat()

    def get_authors(self):
        """Return all authors returned by 'git log'."""
        return set(nt.author for nt in self.nts)

    def get_time2hdrsdata(self):
        """For one time unit, return headers list and files list."""
        time_gitlog = []
        ntobj = cx.namedtuple("ntgitlog", "nthdrs file2hashstat")
        hash2nt_all = {nt.commithash:nt for nt in self.nts}
        for time_cur, file2hashstat in sorted(self.time2file2hashstat.items()):
            # print "FFFFFF", file2hashstat
            nts_cur = [hash2nt_all[h] for h in self.get_hashes(file2hashstat)]
            nthdrs = sorted(nts_cur, key=lambda nt: nt.datetime)
            ntcur = ntobj(nthdrs=nthdrs, file2hashstat=file2hashstat)
            time_gitlog.append((time_cur, ntcur))
        return cx.OrderedDict(time_gitlog)

    @staticmethod
    def get_hashes(file2hash2stat):
        """Get all hashes in one time unit."""
        hashes_all = set()
        for hash2status in file2hash2stat.values():
            hashes_all |= set(hash2status)
        return hashes_all

    @staticmethod
    def _get_data_dictby(data):
        """Convert cx.defaultdict(lambda: cx.defaultdict(list)) to regular dicts."""
        day2data = {day:{} for day in data.keys()}
        for day, filename2hash2stat in data.items():
            for filename, hash2stat in filename2hash2stat.items():
                day2data[day][filename] = hash2stat
        return day2data

    def _get_time2file2hashstat(self):
        """Return 'git log' data organized by day, week, etc..."""
        data = cx.defaultdict(lambda: cx.defaultdict(dict))
        time2nts = cx.defaultdict(list)
        for ntd in self.nts:
            coarse_dt = self.timefnc(ntd.datetime)
            # print "TTTTTTTTTTTTT ({}) ({}) {}".format(ntd.datetime, coarse_dt, repr(ntd.datetime))
            chkin = ntd.commithash
            time2nts[coarse_dt].append(ntd)
            for status, filename in ntd.files:
                data[coarse_dt][filename][chkin] = status
        # Set data members:  time2nt  time2file2hashstat
        self.time2nts = {t:hs for t, hs in time2nts.items()}
        self.time2file2hashstat = self._get_data_dictby(data)


# Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved.
