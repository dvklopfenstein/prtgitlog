"""Run command 'git log ...'. Process and store results."""

__copyright__ = "Copyright (c) 2017-2019, DV Klopfenstein. all rights reserved."
__author__ = "DV Klopfenstein"

import re
import datetime
import collections as cx
import subprocess

class GitLogData(object):
    """Run command 'git log ...'. Process and store results."""

    # PATTERN MATCH EX: d0be326.. d0be326   Author Tue    Apr 26 13:24:19 2016 -0400 pylint
    #                       aa227f1 dvklopfenstein Fri    Jan 26 19:00:06 2018 -0500 :
    #   group number:     1           2       3      4      5                        6
    hdrpat = re.compile(r'(([a-f0-9]+) (\S.*\S) (\S{3}) (\S{3} \d{1,2} \S+ \d{4}) \S+ )')
    hshpat = re.compile(r'([a-f0-9]+) ')
    pretty_fmt = '--pretty=format:"%Cred%H %h %an %cd%Creset %s"'
    ntobj = cx.namedtuple("ntgitlog", "commithash chash author weekday datetime hdr files")

    def __init__(self, kws):
        self.kws = kws
        self.recompile = [re.compile(p) for p in kws['re']] if 're' in kws else None
        self.exclude = [re.compile(p) for p in kws['ve']] if 've' in kws else None
        # Save list of 'git log' command arguments for every 'git log' command to be run:
        #   git log --after "60 days" --pretty=format:"%Cred%H %h %an %cd%Creset %s" --name-status
        self.popencmds = self._init_gitlog_cmds(kws['files'])

    def get_chksum_files(self, noci):
        """Run 'git log' return data in condensed by day."""
        commithash2nt = {}
        for popenargs in self.popencmds:
            self._get_commithash2nt(commithash2nt, popenargs, noci)
        return sorted(commithash2nt.values(), key=lambda nt: nt.datetime, reverse=True)

    def _get_commithash2nt(self, commithash2nt, popenargs, noci):
        """Run 'git log' return data in condensed by day."""
        commitobj = None
        # Run 'git log' command
        gitlog, _ = subprocess.Popen(popenargs, stdout=subprocess.PIPE).communicate() # _ err
        gitlog = gitlog.decode("utf-8")
        for line in gitlog.split('\n'):
            line = line.rstrip()
            ## print('{C:1} LINE={L:1}: {LINE}'.format(
            ##     C=commitobj is not None, L=line != '', LINE=line))
            if line != '':
                # header?: 68f2684... 68f2684 dvklopfenstein Mon Sep 11 16:07:42 2017 -0400 links
                if commitobj is None:
                    # Contains header & empty data list
                    commitobj = self._get_commitobj(line, commithash2nt)
                    ## print('---> commitobj = namedtuple...', commitobj)
                # Data files: 'line' contains filename for one commit
                elif line:
                    commithash = self._re_commithash(line)
                    if commithash is None:
                        self._append_filename(commitobj, line)
                    # Multiple commits found for one file, often occuring with a branch merge
                    else:
                        commitobj = self._get_commitobj(line, commithash2nt)
                # End of Header-files record
            # line is blank and the commit details need to be stored
            elif commitobj is not None:
                ## print('---> commitobj = None', line)
                if noci is None:
                    commithash2nt[commitobj.commithash] = commitobj
                elif commitobj.chash not in noci:
                    commithash2nt[commitobj.commithash] = commitobj
                commitobj = None

    def _append_filename(self, commitobj, line):
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

    def _get_commitobj(self, line, commithash2nt):
        """Return a namedtuple containing header line information."""
        commithash = self._re_commithash(line)
        if commithash is None:
            raise RuntimeError('NO COMMIT HASH({L})'.format(L=line))
        if commithash in commithash2nt:
            return commithash2nt[commithash]
        # Commit information, minus the full hash at the beginning & commit msg at end
        hdrstr = line[len(commithash)+2:]
        mtchhdr = self.hdrpat.search(hdrstr)
        commit_msg = hdrstr[len(mtchhdr.group(1)):].encode('utf-8')
        if commit_msg[-1:] == '"':
            commit_msg = commit_msg[:-1]
        if mtchhdr:
            return self.ntobj(
                commithash=commithash,
                chash=mtchhdr.group(2),
                author=mtchhdr.group(3).encode('utf-8'),
                weekday=mtchhdr.group(4),
                datetime=datetime.datetime.strptime(mtchhdr.group(5), "%b %d %X %Y"),
                hdr=commit_msg,
                files=[])
        raise RuntimeError("**MATCH ERROR: HASH({C}) HEADER({H})\n{L}".format(
            C=commithash, H=line[len(commithash)+2:], L=line))

    def _re_commithash(self, line):
        """Get commit hash from header line"""
        mtch = self.hshpat.search(line)
        if mtch is not None:
            return mtch.group(1)

    def get_gitlog_cmds(self):
        """Return 'git log' command string."""
        return [" ".join(popenargs) for popenargs in self.popencmds]

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

    def _init_gitlog_cmds(self, files):
        """Return 'git log' which prints commit hdr info line followed by a list of files."""
        cmdargs = self._init_gitlog_cmd()
        if not files:
            return [cmdargs]
        return [self._init_gitlog_appendfile(cmdargs, f) for f in files]

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
        if not {'after', 'since'}.isdisjoint(self.kws):
            ret.append('--after')
            ret.append('"{AFTER}"'.format(AFTER=self._get_after()))
        if not {'before', 'until'}.isdisjoint(self.kws):
            ret.append('--before')
            ret.append('"{BEFORE}"'.format(BEFORE=self._get_before()))
        ret.append(self.pretty_fmt)
        ret.append('--name-status')
        return ret

    def _get_after(self):
        """Get starting date for printing git logs"""
        if 'after' in self.kws:
            return self.kws['after']
        if 'since' in self.kws:
            return self.kws['since']

    def _get_before(self):
        """Get ending date for printing git logs"""
        if 'before' in self.kws:
            return self.kws['before']
        if 'until' in self.kws:
            return self.kws['until']

    @staticmethod
    def _init_gitlog_appendfile(cmdargs, filename):
        """Add user-specfied files, if provided"""
        ret = list(cmdargs)
        ret.append('--follow')
        ret.append('--')
        ret.append(filename)
        return ret

# -----------------------------------------------------------------------------------------
# https://stackoverflow.com/questions/424071/how-to-list-all-the-files-in-a-commit
# Preferred Way (because it's a plumbing command; meant to be programmatic):
#     $ git diff-tree --no-commit-id --name-only -r bd61ad98
#     index.html
#     javascript/application.js
#     javascript/ie6.js
#
# Another Way (less preferred for scripts, because it's a porcelain cmd; meant to be user-facing)
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
