# gitlog
A script to print **_git log_** output in a **concise** and **informative** format

## Example Uses

  1. [**Get information for your weekly status report**](#1-get-information-for-your-weekly-status-report)
  2. [**Get information for your annual review**](#2-get-information-for-your-annual-review)

### 1) Get information for your weekly status report
Or on Monday morning, remind yourself what you did last week.

#### The reports are split into two sections:
  1. **Commit information**. Each commit is given an alias (e.g., A, B, C, D, E, ...)
  2. A list of **files** that were commited and thier commit aliases    
     M->Modified, A->Added, R->Removed

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
Get all commits donw in the last year, grouped by month:
```
$ gitlog --month --after='365 days'
```

## Succinct Output: A Comparison

| Description           | # Lines | Example Output Codeblock
|-----------------------|---------|-------------------------
| _git log_ COMMAND     |      70 | [git log --after "2 days"](doc/md/README_example_succint_cmdline.md)
| _gitlog_ REPO SCRIPT  |      10 | [gitlog --after="2 days"](doc/md/README_example_succint_script.md)


Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
