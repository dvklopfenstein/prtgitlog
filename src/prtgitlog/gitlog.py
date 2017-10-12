#!/usr/bin/env python
"""Clearly and concisely report each day's 'git log' commits."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import sys
import datetime

from prtgitlog.data import GitLogData
from prtgitlog.sortbytime import GitLogByTime
from prtgitlog.prthdrs import PrtHdrs

class GitLog(object):
    """Organize file revision information from a repository in GitHub."""

    hdr_section = "\n{DATE} {Mon}\n" # Section header. Sections are by day, week, or month
    #hdrpat_dflt = "  {weekday} {datetime} {chash} {abc} {author} {hdr}\n"
    hdrpat_dflt = "  {weekday} {datetime} {chash} {abc} {hdr}\n"

    def __init__(self, **kws):
        _ini = GitLogData(kws.get('after', "2016-01-12"), kws.get('re', None), kws.get('ve', None))
        self.gitlog_cmd = _ini.get_gitlog_cmd()
        self.ntsgitlog = _ini.get_chksum_files(kws.get('noci', None))
        self.hdrpat = kws.get('hdrpat', self.hdrpat_dflt)
        self.timegrain = {
            'by_day':self.by_day,
            'by_week':self.by_week,
            'by_month':self.by_month,
        }

    @staticmethod
    def by_day(cur_datetime):
        """Given a full datetime object, return a datetime object for the day."""
        return datetime.datetime(cur_datetime.year, cur_datetime.month, cur_datetime.day)

    @staticmethod
    def by_week(cur_datetime):
        """Given a full datetime object, return a datetime object for the week."""
        # A week starts on Monday and ends on Sunday
        iso_year, iso_wk, _ = cur_datetime.isocalendar() # ISO: year, week, day
        fourth_jan = datetime.date(iso_year, 1, 4)
        delta = datetime.timedelta(fourth_jan.isoweekday()-1)
        iso_year_start = fourth_jan - delta
        #date = iso_year_start + datetime.timedelta(days=iso_day-1, weeks=iso_wk-1)
        date = iso_year_start + datetime.timedelta(days=0, weeks=iso_wk-1)
        return date

    @staticmethod
    def by_month(cur_datetime):
        """Given a full datetime object, return a datetime object for the month."""
        return datetime.datetime(cur_datetime.year, cur_datetime.month, 1)

    def run(self, by_time='by_day', prt=sys.stdout):
        """Print git logs for 1 day at a time. Print the day's edited files once."""
        objtimedata = GitLogByTime(self.ntsgitlog, self.timegrain[by_time])
        self.prt_time2gitlog(objtimedata, prt)

    def prt_time2gitlog(self, objtime, prt=sys.stdout):
        """Print 'git log' data by day."""
        for day, ntday in objtime.get_time2hdrsdata().items():
            if ntday.file2hashes is not None:
                self._prt_timegroup(prt, day, ntday)
        prt.write("\nRAN: {CMD}\n".format(CMD=self.gitlog_cmd))

    def _prt_timegroup(self, prt, day, ntday):
        """Print header lines and filenames for one time group."""
        # nts_cur = objtime.time2nts[day]
        nts_cur = ntday.nthdrs # Default: prt just hdrs in re
        objhdr = PrtHdrs(nts_cur, ntday.file2hashes)
        prt.write(self.hdr_section.format(Mon=day.strftime('%a'), DATE=day.strftime("%Y_%m_%d")))
        objhdr.prt_hdrs(self.hdrpat, prt)
        for ntd in sorted(objhdr.ntdat, key=lambda n: [n.letterstr, n.filename], reverse=True):
            prt.write("    {CIs} {DATA}\n".format(CIs=ntd.letterstr, DATA=ntd.filename))

    # @staticmethod
    # def ls_tree():
    #   """Get a list of all files stored in the git repo."""
    #   popenargs = ['git', 'ls-tree', '--full-tree', '-r', '--name-only', 'HEAD'] # git cmd
    #   gitlogcmd, _ = subprocess.Popen(popenargs, stdout=subprocess.PIPE).communicate() # cmd, err
    #   return [os.path.join(".", line.rstrip()) for line in gitlogcmd.split('\n')]



# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
