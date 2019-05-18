"""Run command 'git log ...'. Process and store results."""

__copyright__ = "Copyright (c) 2017-2019, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import re
import datetime
import collections as cx
import subprocess

class GitLogData(object):
    """Run command 'git log ...'. Process and store results."""

    # PATTERN MATCH EX:  d0be326.. d0be326   Author Tue    Apr 26 13:24:19 2016 -0400 pylint
    #   group number:      1           2       3      4      5                        6
    hdrpat_dflt = r'([a-f0-9]+) (\S+) (\S.*\S) (\S{3}) (\S{3} \d{1,2} \S+ \d{4}) \S+ (\S.*\S)"'
    pretty_fmt = '--pretty=format:"%Cred%H %h %an %cd%Creset %s"'
    ntobj = cx.namedtuple("ntgitlog", "commithash chash author weekday datetime hdr files")

    #### def __init__(self, after="2016-01-12", restr=None, ve_list=None):
    def __init__(self, kws):
        self.after = kws.get('after', None)
        self.recompile = [re.compile(p) for p in kws['re']] if 're' in kws else None
        self.exclude = [re.compile(p) for p in kws['ve']] if 've' in kws else None
        # Ex: git log --after "60 days" --pretty=format:"%Cred%H %h %an %cd%Creset %s" --name-status
        self.popenargs = self._init_gitlog_cmd()

    def get_chksum_files(self, noci):
        """Run 'git log' return data in condensed by day."""
        data = []
        hdrpat = re.compile(self.hdrpat_dflt)
        commitobj = None
        # # Run 'git log' command
        gitlog, _ = subprocess.Popen(self.popenargs, stdout=subprocess.PIPE).communicate() # _ err
        for line in gitlog.split('\n'):
            line = line.rstrip()
            # header?: 68f2684... 68f2684 dvklopfenstein Mon Sep 11 16:07:42 2017 -0400 links
            if commitobj is None:
                commitobj = self._get_commitobj(line, hdrpat)  # Contains header & empty data list
            # Data files: 'line' contains filename for one commit
            elif line:
                self._append_data(commitobj, line)
            # End of Header-files record
            else: # line is blank
                assert commitobj is not None
                if noci is None:
                    data.append(commitobj)
                elif commitobj.chash not in noci:
                    data.append(commitobj)
                commitobj = None
        return data

    def _append_data(self, commitobj, line):
        """Fill commit object with filename."""
        if self._test_filename_regex(line):
            status_file = line.split()
            if line[0] == 'R':
                status = status_file[0]
                status_file = line.split()
                commitobj.files.append((status, status_file[1]))
                commitobj.files.append((status, status_file[2]))
            else:
                commitobj.files.append((line[0], line[1:].strip()))
            # else:
            #     raise RuntimeError("UNKNOWN DATA({D}).\nHDR({H})".format(D=line, H=commitobj))

    def _get_commitobj(self, line, hdrpat):
        """Return a namedtuple containing header line information."""
        mtchhdr = hdrpat.search(line)
        if mtchhdr:
            return self.ntobj(
                commithash=mtchhdr.group(1),
                chash=mtchhdr.group(2),
                author=mtchhdr.group(3),
                weekday=mtchhdr.group(4),
                datetime=datetime.datetime.strptime(mtchhdr.group(5), "%b %d %X %Y"),
                hdr=mtchhdr.group(6),
                files=[])
        assert "BAD HEADER({H})".format(H=line)

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
        if self.recompile is not None:
            for srch in self.recompile:
                if srch.search(line):
                    return True
        return False

    def _init_gitlog_cmd(self):
        """Return 'git log' which prints commit hdr info line followed by a list of files."""
        #
        # % git log --after "10 days" --pretty=format:"%Cred%h %cd%Creset %s" --name-only
        # aa4bb03 Mon Sep 11 16:09:39 2017 -0400 Added script to add links to markdown D1/G9a
        # M doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_Ezh2.py
        # M doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_G9a.py
        # M doc/images/y2014mozzetta_g9a_bw_d1_plots/plotit_Mozzetta2014_ivls15_PRC2.py
        # M src/bin/compare_d1g9a_ivls_md_update.py
        #
        # 68f2684 Mon Sep 11 16:07:42 2017 -0400 links
        # M data/2014_Mozzetta/README.md
        #
        #cmd = 'git log --after "{AFTER}" --pretty=format:"%Cred%h %cd%Creset %s" --name-only'
        ret = ['git', 'log']
        if self.after is not None:
            ret.append('--after')
            ret.append('"{AFTER}"'.format(AFTER=self.after))
        return ret + [self.pretty_fmt, '--name-status']

# -----------------------------------------------------------------------------------------
# https://stackoverflow.com/questions/424071/how-to-list-all-the-files-in-a-commit
# Preferred Way (because it's a plumbing command; meant to be programmatic):
#     $ git diff-tree --no-commit-id --name-only -r bd61ad98
#     index.html
#     javascript/application.js
#     javascript/ie6.js
# 
# Another Way (less preferred for scripts, because it's a porcelain command; meant to be user-facing)
#     $ git show --pretty="" --name-only bd61ad98    
#     index.html
#     javascript/application.js
#     javascript/ie6.js

# If you want to get list of changed files:
#     git diff-tree --no-commit-id --name-only -r <commit-ish>
# If you want to get list of all files in a commit, you can use
#     git ls-tree --name-only -r <commit-ish>

#     $ git show --stat --oneline HEAD

# -----------------------------------------------------------------------------------------
# How to list all commits that changed a specific file?
# https://stackoverflow.com/questions/3701404/how-to-list-all-commits-that-changed-a-specific-file
#
# The --follow works for a particular file (and follows renames)
#     $ git log --follow -- filename
#
# NOTE: +1 --follow accounts for renames, so this is more robust than git log -- path 


# Copyright (c) 2017-2019, DV Klopfenstein. all rights reserved.
