"""Run command 'git log ...' and return results."""

__copyright__ = "Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import re
import datetime
import collections as cx
import subprocess

class GitLogData(object):
    """Run command 'git log ...' and return results."""

    # PATTERN MATCH EX:  d0be326.. d0be326   Author Tue    Apr 26 13:24:19 2016 -0400 pylint
    #   group number:      1           2       3      4      5                        6
    hdrpat_dflt = r'([a-f0-9]+) (\S+) (\S+) (\S{3}) (\S{3} \d+ \S+ \d{4}) \S+ (\S.*\S)"'
    pretty_fmt = '--pretty=format:"%Cred%H %h %an %cd%Creset %s"'

    def __init__(self, after="2016-01-12", restr=None, ve_list=None):
        self.after = after
        self.recompile = None if restr is None else re.compile(restr)
        self.exclude = None if ve_list is None else [re.compile(ve) for ve in ve_list]
        self.popenargs = self._init_gitlog_cmd()

    def get_chksum_files(self, noci):
        """Run 'git log' return data in condensed by day."""
        data = []
        hdrpat = re.compile(self.hdrpat_dflt)
        ntobj = cx.namedtuple("ntgitlog", "commithash chash author weekday datetime hdr files")
        commitdata = None
        # # Run 'git log' command
        gitlog, _ = subprocess.Popen(self.popenargs, stdout=subprocess.PIPE).communicate() # err
        for line in gitlog.split('\n'):
            line = line.rstrip()
            # header?: 68f2684... 68f2684 dvklopfenstein Mon Sep 11 16:07:42 2017 -0400 links
            if commitdata is None:
                mtchhdr = hdrpat.search(line)
                if mtchhdr:
                    commitdata = ntobj(
                        commithash=mtchhdr.group(1),
                        chash=mtchhdr.group(2),
                        author=mtchhdr.group(3),
                        weekday=mtchhdr.group(4),
                        datetime=datetime.datetime.strptime(mtchhdr.group(5), "%b %d %X %Y"),
                        hdr=mtchhdr.group(6),
                        files=[])
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
        # aa4bb03 Mon Sep 11 16:09:39 2017 -0400 Added script to add links to markdown D1/G9a
        # doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_Ezh2.py
        # doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_G9a.py
        # doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_PRC2.py
        # src/bin/compare_d1g9a_ivls_md_update.py
        #
        # 68f2684 Mon Sep 11 16:07:42 2017 -0400 links
        # data/2014_Mozzetta/README.md
        #
        #cmd = 'git log --after "{AFTER}" --pretty=format:"%Cred%h %cd%Creset %s" --name-only'
        astr = '"{AFTER}"'.format(AFTER=self.after)
        return ['git', 'log', '--after', astr, self.pretty_fmt, '--name-only']

# Copyright (c) 2014-2017, DV Klopfenstein. all rights reserved.
