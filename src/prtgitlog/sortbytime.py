"""Return data from 'git log' organized by coarse time unit."""

__copyright__ = "Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved."
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
        # Set data members:  time2nt  time2file2hashstat
        data = cx.defaultdict(lambda: cx.defaultdict(dict))
        if self.timefnc is not None:
            time2nts, time2file2hashstat = self._get_time2vars_bytime(data)
        else:
            time2nts, time2file2hashstat = self._get_time2vars_ungrouped(data)
        self.time2nts = time2nts
        self.time2file2hashstat = time2file2hashstat

    def _get_time2vars_bytime(self, data):
        """Return 'git log' data organized by day, week, etc..."""
        time2nts = cx.defaultdict(list)
        for ntd in self.nts:
            coarse_dt = self.timefnc(ntd.datetime)
            # print("TTTTTTTTTTT ({}) ({}) {}".format(ntd.datetime, coarse_dt, repr(ntd.datetime)))
            time2nts[coarse_dt].append(ntd)
            self._fill_data(data, ntd, coarse_dt)
        return {t:hs for t, hs in time2nts.items()}, self._get_data_dictby(data)

    def _get_time2vars_ungrouped(self, data):
        """Return 'git log' data as a single list."""
        assert self.nts[0].datetime >= self.nts[-1].datetime, '**ERROR: {} >= {}'.format(
            self.nts[0].datetime, self.nts[-1].datetime)
        time_key = self.nts[-1].datetime
        for ntd in self.nts:
            self._fill_data(data, ntd, time_key)
        return {time_key: self.nts}, self._get_data_dictby(data)

    @staticmethod
    def _fill_data(data, ntd, time_key):
        """Fill this time unit with git log information for all files."""
        chkin = ntd.commithash
        for status, filename in ntd.files:
            data[time_key][filename][chkin] = status

# Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
