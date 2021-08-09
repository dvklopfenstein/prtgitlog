# gitlog
[![DOI](/doc/md/images/zenodo.3066256.svg)](https://doi.org/10.5281/zenodo.3066256)
[![Latest PyPI version](https://img.shields.io/pypi/v/prtgitlog.svg)](https://pypi.python.org/pypi/prtgitlog)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Anaconda-Server Badge](https://anaconda.org/dvklopfenstein/prtgitlog/badges/version.svg)](https://anaconda.org/dvklopfenstein/prtgitlog)    
A script to print **_git log_** output in a **concise** and **informative** format

## Installation
```
pip install prtgitlog
```
or
```
conda install -c dvklopfenstein prtgitlog
```
## Example Uses

Get:    

  1. [**Information for your weekly status report**](#1-get-information-for-your-weekly-status-report)
  2. [**Information for your annual review**](#2-get-information-for-your-annual-review)
  3. [**All information for one or more files**](#3-get-all-information-for-one-or-more-files)


### 1) Get information for your weekly status report
Or on Monday morning, remind yourself what you did last week.

#### The reports are split into two sections:
  1. **Commit information**. Each commit is given an alias (e.g., A, B, C, D, E, ...)
  2. A list of **files** that were commited, preceded by thier commit aliases    

#### Example
Get commits during the last 7 days, grouped by week:
```
$ gitlog --week --after='7 days'

Week STARTING ON: 2019_05_13 Mon - 11 commits, 10 files
  Fri 2019-05-17 11:41:27 1bc99eb A Added links to examples of git commands
  Sat 2019-05-18 05:49:27 3430cd1 B Add FILES argument
  Sat 2019-05-18 05:50:52 1943ce5 C Add STARTING ON for clarity
  Sat 2019-05-18 06:33:10 9bb5654 D Implement git log follow for user-specified files
  Sun 2019-05-19 04:28:45 360db18 E Allow multiple 'git log's to be run
  Sun 2019-05-19 05:03:43 3703854 F Run 'git log' on multiple user-specified files
  Sun 2019-05-19 05:11:29 d4106b2 G Opening README line more concise
  Sun 2019-05-19 12:04:00 95a7b7b H Handle consecutive empty lines in 'git log' output
  Sun 2019-05-19 12:08:54 3544c8a I Get grouping at runtime if not user-specified
  Sun 2019-05-19 12:12:28 3f2bf25 J If numerous 'git log' commands used: write to a log file
  Sun 2019-05-19 12:20:46 3c86b31 K Clearer, more concise doc
    A..DEF.H... M src/prtgitlog/gitlog_strm.py
    .B.DEF..I.K M src/prtgitlog/cli.py
    ..CD....I.. M src/prtgitlog/prtlog.py
    ...DE...... M src/prtgitlog/sortbytime.py
    ...D.F..IJ. M src/prtgitlog/gitlog.py
    ...D.F..I.. M src/tests/test_cli.py
    ......G...K M README.md
    ........I.. M src/prtgitlog/commit_info.py
    ........I.. M src/prtgitlog/commit_files.py
    ........I.. M src/bin/gitlog.py
```

### 2) Get information for your annual review
Get all commits done in the last year, grouped by month:
```
$ gitlog --month --after='365 days'
```

### 3) Get all information for one or more files
Get all commits for two files:
  * src/prtgitlog/commit_aliases.py
  * src/prtgitlog/commit_files.py

Notice that the log follows a file that is renamed:    
  * src/prtgitlog/prthdrs.py -> src/prtgitlog/commit_aliases.py

In the files section, after the commit aliases:
  * M: Modified
  * A: Added
  * R: Removed

#### Example
```
$ gitlog src/prtgitlog/commit_aliases.py src/prtgitlog/commit_files.py

All STARTING ON: 2017_09_29 Fri - 12 commits, 3 files
  Fri 2017-09-29 11:10:52 72bb16e A Put each class into its own module.
  Thu 2017-10-12 11:21:36 c0dc685 B pylint. Add vim target
  Thu 2017-10-12 14:13:06 2d0f281 C Now printing status for each file's commit.
  Tue 2018-01-02 16:03:33 fac8edd D Limit rev chrs to printable characters
  Tue 2018-01-09 14:13:43 7b44fbd E Updated Copyright date to 2018.
  Thu 2018-01-18 12:02:43 b90f8c9 F cleanup. Beginning to add date-fmt headers.
  Sat 2018-01-20 10:33:33 9c4b8bb G Moved commit aliases to commit_aliases filename (better desc)
  Mon 2018-01-22 14:43:42 dfc1993 H SPlit commit aliases apart from commit info and commit files.
  Tue 2018-01-23 15:23:53 b0b2e11 I Adjust status size to max status letters
  Fri 2018-01-26 19:08:26 1563e0f J Changed Copyright to 2017-2018
  Sat 2019-05-18 05:51:36 dab53ee K update copyright date
  Sun 2019-05-19 12:08:54 3544c8a L Determine bytime grouping at runtime if not user-specified
    ABCDEFG..... AMR src/prtgitlog/prthdrs.py
    ......GH.JK.  RM src/prtgitlog/commit_aliases.py
    .......HIJKL  AM src/prtgitlog/commit_files.py
```


## Succinct Output: A Comparison

| Description           | # Lines | Example Output Codeblock
|-----------------------|---------|-------------------------
| _git log_ COMMAND     |      70 | [git log --after "2 days"](doc/md/README_example_succint_cmdline.md)
| _gitlog_ REPO SCRIPT  |      10 | [gitlog --after="2 days"](doc/md/README_example_succint_script.md)


[webpage](https://dvklopfenstein.github.io/prtgitlog/)
Copyright (C) 2017-present, DV Klopfenstein. All rights reserved.
