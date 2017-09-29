#!/usr/bin/env python
"""Clearly and concisely report each day's 'git log' commits."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import sys
import datetime
import re
import collections as cx
import subprocess

class GitLog(object):
  """Organize file revision information from a repository in GitHub."""

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
        # nts_cur = objtime.time2nts[day]
        nts_cur = ntday.nthdrs # Default: prt just hdrs in re
        objhdr = PrtHdrs(nts_cur, ntday.file2hashes)
        prt.write("\n{DATE} {Mon}\n".format(Mon=day.strftime('%a'), DATE=day.strftime("%Y_%m_%d")))
        objhdr.prt_hdrs(self.hdrpat, prt)
        for ntd in sorted(objhdr.ntdat, key=lambda n: [n.letterstr, n.filename], reverse=True):
          prt.write("    {CIs} {DATA}\n".format(CIs=ntd.letterstr, DATA=ntd.filename))
    prt.write("\nRAN: {CMD}\n".format(CMD=self.gitlog_cmd))

  # @staticmethod
  # def ls_tree():
  #   """Get a list of all files stored in the git repo."""
  #   popenargs = ['git', 'ls-tree', '--full-tree', '-r', '--name-only', 'HEAD'] # git cmd
  #   gitlogcmd, _ = subprocess.Popen(popenargs, stdout=subprocess.PIPE).communicate() # cmd, err
  #   return [os.path.join(".", line.rstrip()) for line in gitlogcmd.split('\n')]


class PrtHdrs(object):
  """Print 'git log' headers."""

  def __init__(self, nts_cur, file2hashes):
    self.nthdrs = sorted(nts_cur, key=lambda nt:nt.datetime)
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
      nts_cur = [hash2nt_all[h] for h in self._get_hashes(file2hashes.values())]
      nthdrs = sorted(nts_cur, key=lambda nt: nt.datetime)
      ntcur = ntobj(nthdrs=nthdrs, file2hashes=file2hashes)
      time_gitlog.append((time_cur, ntcur))
    #time_gitlog = [(t, ntobj(nthdrs=nthdrs[t], data=time2items.get(t, None))) for t in times]
    return cx.OrderedDict(time_gitlog)

  @staticmethod
  def _get_hashes(commithashes):
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


class GitLogData(object):
  """Run command 'git log ...' and return results."""

  pretty_fmt = '--pretty=format:"%Cred%H %h %an %cd%Creset %s"'

  def __init__(self, after="2016-01-12", recompile=None, exclude=None):
    self.after = after
    self.recompile = self._init_re(recompile)
    self.exclude = self._init_ve(exclude)
    self.popenargs = self._init_gitlog_cmd()

  def get_chksum_files(self, noci):
    """Run 'git log' return data in condensed by day."""
    data = []
    # PATTERN MATCH EX:  d0be326.. d0be326   Author Tue    Apr 26 13:24:19 2016 -0400 pylint
    #   group number:      1           2       3      4      5                        6
    hdrpat = re.compile(r'([a-f0-9]+) (\S+) (\S+) (\S{3}) (\S{3} \d+ \S+ \d{4}) \S+ (\S.*\S)"')
    ntobj = cx.namedtuple("ntgitlog", "commithash chash author weekday datetime hdr files")
    commitdata = None
    # # Run 'git log' command
    gitlog, _ = subprocess.Popen(self.popenargs, stdout=subprocess.PIPE).communicate() # gitlog, err
    for line in gitlog.split('\n'):
      line = line.rstrip()
      # Check for a header: 68f2684... 68f2684 dvklopfenstein Mon Sep 11 16:07:42 2017 -0400 links
      if commitdata is None:
        mtchhdr = hdrpat.search(line)
        if mtchhdr:
          commitdata = ntobj(
              commithash = mtchhdr.group(1),
              chash = mtchhdr.group(2),
              author = mtchhdr.group(3),
              weekday = mtchhdr.group(4),
              datetime = datetime.datetime.strptime(mtchhdr.group(5), "%b %d %X %Y"),
              hdr = mtchhdr.group(6),
              files = [])
      # Data files: 'line' contains filename for one commit
      elif line:
        if self._test_filename_regex(line):
          commitdata.files.append(line)
      # End of Header-files record
      else: # line is blank
        assert commitdata is not None
        if noci is None:
          data.append(commitdata)
        elif commitdata.chash not in noci:
          data.append(commitdata)
        commitdata = None
    return data

  def get_gitlog_cmd(self):
    """Return 'git log' command string."""
    return " ".join(self.popenargs)

  def _test_filename_regex(self, line):
    """Return True if this line should be saved."""
    if self.recompile is None and self.exclude is None:
      return True
    if self.exclude is not None:
      for recmp in self.exclude:
        if recmp.search(line):
          return False
    mtch_re = None
    if self.recompile is not None:
      mtch_re = self.recompile.search(line)
    return True if mtch_re else False

  def _init_gitlog_cmd(self):
    """Return 'git log' which prints commit hdr info line followed by a list of files."""
    #
    # % git log --after "10 days" --pretty=format:"%Cred%h %cd%Creset %s" --name-only
    # aa4bb03 Mon Sep 11 16:09:39 2017 -0400 Added script to add links to markdown D1/G9a loci table
    # doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_Ezh2.py
    # doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_G9a.py
    # doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_PRC2.py
    # src/bin/compare_d1g9a_ivls_md_update.py
    #
    # 68f2684 Mon Sep 11 16:07:42 2017 -0400 links
    # data/2014_Mozzetta/README.md
    #
    #cmd = 'git log --after "{AFTER}" --pretty=format:"%Cred%h %cd%Creset %s" --name-only > {FOUT}'
    astr = '"{AFTER}"'.format(AFTER=self.after)
    return ['git', 'log', '--after', astr, self.pretty_fmt, '--name-only']

  @staticmethod
  def _init_re(restr):
    """Initialize filename regex compile."""
    if restr is None:
      return None
    return re.compile(restr)

  @staticmethod
  def _init_ve(ve_list):
    """Initialize filename regex compile."""
    if ve_list is None:
      return None
    return [re.compile(ve) for ve in ve_list]

# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
