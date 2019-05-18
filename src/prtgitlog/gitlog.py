#!/usr/bin/env python
"""Clearly and concisely report each day's 'git log' commits."""

__copyright__ = "Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import datetime

from prtgitlog.gitlog_strm import GitLogData
from prtgitlog.sortbytime import GitLogByTime
from prtgitlog.prtlog import PrtLog

class GitLog(object):
    """Organize file revision information from a repository in GitHub."""

    def __init__(self, kws, keys):
        self.kws = kws
        self.keys = keys
        _ini = GitLogData(kws)
        self.gitlog_cmd = _ini.get_gitlog_cmd()
        # namedtuple fields: commithash chash author weekday datetime hdr files
        self.ntsgitlog = _ini.get_chksum_files(kws.get('noci', None))
        self.timegrain = {
            'day':self.by_day,
            'week':self.by_week,
            'month':self.by_month,
            'year':self.by_year,
            'all':None,
        }

    def run(self, by_time='by_month', prt=sys.stdout):
        """Print git logs for 1 day at a time. Print the day's edited files once."""
        if self.ntsgitlog:
            objtimedata = GitLogByTime(self.ntsgitlog, self.timegrain[by_time])
            objprtlog = PrtLog(objtimedata, self.kws, self.keys)
            objprtlog.prt_time2gitlog(prt)
            prt.write("{N} commits since {DATE} shown\n".format(
                N=len(self.ntsgitlog), DATE=self.ntsgitlog[-1].datetime.strftime("%Y_%m_%d")))
        prt.write("\nRAN: {CMD}\n".format(CMD=self.gitlog_cmd))

    @staticmethod
    def by_day(cur_datetime):
        """Given a full datetime object, return a datetime object for the day."""
        return datetime.datetime(cur_datetime.year, cur_datetime.month, cur_datetime.day)

    @staticmethod
    def by_week(cur_datetime):
        """Given a full datetime object, return a datetime object for the week."""
        # A week starts on Monday and ends on Sunday
        iso_year, iso_week, _ = cur_datetime.isocalendar() # ISO: year, week, day
        fourth_jan = datetime.date(iso_year, 1, 4)
        delta = datetime.timedelta(fourth_jan.isoweekday()-1)
        iso_year_start = fourth_jan - delta
        #date = iso_year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)
        date = iso_year_start + datetime.timedelta(days=0, weeks=iso_week-1)
        return date

    @staticmethod
    def by_month(cur_datetime):
        """Given a full datetime object, return a datetime object for the month."""
        return datetime.datetime(cur_datetime.year, cur_datetime.month, 1)

    @staticmethod
    def by_year(cur_datetime):
        """Given a full datetime object, return a datetime object for the year."""
        return datetime.datetime(cur_datetime.year, 1, 1)

    # @staticmethod
    # def ls_tree():
    #   """Get a list of all files stored in the git repo."""
    #   popenargs = ['git', 'ls-tree', '--full-tree', '-r', '--name-status', 'HEAD'] # git cmd
    #   gitlogcmd, _ = subprocess.Popen(popenargs, stdout=subprocess.PIPE).communicate() # cmd, err
    #   return [os.path.join(".", line.rstrip()) for line in gitlogcmd.split('\n')]


# Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
