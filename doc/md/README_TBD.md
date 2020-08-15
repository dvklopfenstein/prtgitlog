## Examples

### Grouping aruguments
**Group** commits by day, week, month, year, or ungrouped (all)     
```
$ gitlog --week
$ gitlog --month
$ gitlog --year
$ gitlog --day
$ gitlog --all
```

  * Print all '[git log](https://git-scm.com/docs/git-log)' data, grouped by **week**
  * Print all '[git log](https://git-scm.com/docs/git-log)' data, grouped by **month**
  * Print all '[git log](https://git-scm.com/docs/git-log)' data, grouped by **year**
  * Print all '[git log](https://git-scm.com/docs/git-log)' data, grouped by **day**
  * Print all '[git log](https://git-scm.com/docs/git-log)' data, **not grouped by any time unit**
  * **Succinct Date-only header**    
```
    gitlog --all --hdr=date
```

### By week (default)

```
% gitlog

2018_01_01 Mon
  Tue 2018-01-02 15:33:38 bbab23a A Added byyear
  Tue 2018-01-02 16:03:33 fac8edd B Limit rev chrs to printable characters. Re-use chrs if large number of revisions.
  Tue 2018-01-02 17:10:03 fd75626 C Starting to switch to docopt
  Thu 2018-01-04 11:26:48 6cd897e D Added --re and after to docopt options
  Thu 2018-01-04 11:36:57 6c15dec E Removed unused keyword, bytime
    A.CDE  M src/prtgitlog/cli.py
    A.CD.  M src/prtgitlog/gitlog.py
    A.C..  M src/bin/gitlog.py
    .B...  M src/prtgitlog/prthdrs.py
    ...D.  M src/prtgitlog/data.py

2018_01_08 Mon
  Tue 2018-01-09 14:07:46 746e818 A Collect author, even if author is more than one word. Print author if there are many authors.
  Tue 2018-01-09 14:13:43 7b44fbd B Updated Copyright date to 2018.
  Tue 2018-01-09 14:17:41 9cd5340 C Added TBD comments
  Tue 2018-01-09 23:01:54 9d06509 D starting setup.py + info
  Wed 2018-01-10 12:19:07 a3da58d E Removed ununsed keyword arg with value, None.
  Wed 2018-01-10 12:59:31 9c0e656 F Started to work on converting DAYS arg. Added cli test.
  Wed 2018-01-10 13:33:10 c1156e4 G Added support for specifing all git logs after N days
  Wed 2018-01-10 13:34:37 a80e34f H minor doc change
  Sat 2018-01-13 12:57:36 4f21b5a I Just using docopt now. Added option to not group git logs by any time unit (just a single list)
  Sat 2018-01-13 13:19:55 b5ead74 J started author
  Sun 2018-01-14 18:50:28 4c1ac38 K Added options: au and fullhash
    AB..E.G..JK  M src/prtgitlog/data.py
    AB......I.K  M src/prtgitlog/gitlog.py
    AB......I..  M src/prtgitlog/sortbytime.py
    AB........K  M src/prtgitlog/prtlog.py
    A..........  M .pylintrc
    .BC.EFGHIJK  M src/prtgitlog/cli.py
    .B..EF..I.K  M src/bin/gitlog.py
    .B.........  M src/prtgitlog/prthdrs.py
    .B.........  M README.md
    ...D.......  M src/prtgitlog/__init__.py
    ...D.......  A setup.py
    ....EF.....  M makefile
    .....FG.... AM src/tests/test_cli.py
```

### By month

```
% gitlog --month

2018_01_01 Mon
  Tue 2018-01-02 15:33:38 bbab23a A Added byyear
  Tue 2018-01-02 16:03:33 fac8edd B Limit rev chrs to printable characters. Re-use chrs if large number of revisions.
  Tue 2018-01-02 17:10:03 fd75626 C Starting to switch to docopt
  Thu 2018-01-04 11:26:48 6cd897e D Added --re and after to docopt options
  Thu 2018-01-04 11:36:57 6c15dec E Removed unused keyword, bytime
  Tue 2018-01-09 14:07:46 746e818 F Collect author, even if author is more than one word. Print author if there are many authors.
  Tue 2018-01-09 14:13:43 7b44fbd G Updated Copyright date to 2018.
  Tue 2018-01-09 14:17:41 9cd5340 H Added TBD comments
  Tue 2018-01-09 23:01:54 9d06509 I starting setup.py + info
  Wed 2018-01-10 12:19:07 a3da58d J Removed ununsed keyword arg with value, None.
  Wed 2018-01-10 12:59:31 9c0e656 K Started to work on converting DAYS arg. Added cli test.
  Wed 2018-01-10 13:33:10 c1156e4 L Added support for specifing all git logs after N days
  Wed 2018-01-10 13:34:37 a80e34f M minor doc change
  Sat 2018-01-13 12:57:36 4f21b5a N Just using docopt now. Added option to not group git logs by any time unit (just a single list)
  Sat 2018-01-13 13:19:55 b5ead74 O started author
  Sun 2018-01-14 18:50:28 4c1ac38 P Added options: au and fullhash
  Mon 2018-01-15 15:54:34 d6a9eca Q Can now match multiple searches.
  Mon 2018-01-15 15:55:05 03b604b R rm debug prints
  Wed 2018-01-17 12:25:12 dd36ec6 S Sort data by alias or by filename
    A.CDE.GH.JKLMNOPQRS  M src/prtgitlog/cli.py
    A.CD.FG......N.P..S  M src/prtgitlog/gitlog.py
    A.C...G..JK..N.P..S  M src/bin/gitlog.py
    .B....G............  M src/prtgitlog/prthdrs.py
    ...D.FG..J.L..OPQ..  M src/prtgitlog/data.py
    .....FG......N.....  M src/prtgitlog/sortbytime.py
    .....FG........P..S  M src/prtgitlog/prtlog.py
    .....F.............  M .pylintrc
    ......G............  M README.md
    ........I..........  M src/prtgitlog/__init__.py
    ........I..........  A setup.py
    .........JK........  M makefile
    ..........KL....Q.. AM src/tests/test_cli.py
```

### Ungrouped (Show all changes)
```
% gitlog --all

2017_09_29 Fri
  Fri 2017-09-29 10:24:53 91c1305 A Initial commit
  Fri 2017-09-29 10:26:39 99ccf46 B Add git log files.
  Fri 2017-09-29 10:28:09 a29b6c3 C Changed pkg name to prtgitlog
  Fri 2017-09-29 11:10:52 72bb16e D Put each class into its own module.
  Thu 2017-10-12 11:21:36 c0dc685 E pylint. Add vim target
  Thu 2017-10-12 14:13:06 2d0f281 F Now printing status for each file's commit.
  Thu 2017-10-12 14:26:05 222e836 G Handle files which have spaces in their name
  Fri 2017-10-13 14:37:19 3f3396b H Made default 'by_week', rather than 'by_day'
  Mon 2017-10-16 12:19:22 1aea5ee I If status letters are repeated, collapse them in the summary print.
  Tue 2017-10-17 08:28:40 9937c89 J Start using docopt
  Tue 2017-10-17 08:55:37 8ccb011 K print kws
  Tue 2018-01-02 15:33:38 bbab23a L Added byyear
  Tue 2018-01-02 16:03:33 fac8edd M Limit rev chrs to printable characters. Re-use chrs if large number of revisions.
  Tue 2018-01-02 17:10:03 fd75626 N Starting to switch to docopt
  Thu 2018-01-04 11:26:48 6cd897e O Added --re and after to docopt options
  Thu 2018-01-04 11:36:57 6c15dec P Removed unused keyword, bytime
  Tue 2018-01-09 14:07:46 746e818 Q Collect author, even if author is more than one word. Print author if there are many authors.
  Tue 2018-01-09 14:13:43 7b44fbd R Updated Copyright date to 2018.
  Tue 2018-01-09 14:17:41 9cd5340 S Added TBD comments
  Tue 2018-01-09 23:01:54 9d06509 T starting setup.py + info
  Wed 2018-01-10 12:19:07 a3da58d U Removed ununsed keyword arg with value, None.
  Wed 2018-01-10 12:59:31 9c0e656 V Started to work on converting DAYS arg. Added cli test.
  Wed 2018-01-10 13:33:10 c1156e4 W Added support for specifing all git logs after N days
  Wed 2018-01-10 13:34:37 a80e34f X minor doc change
  Sat 2018-01-13 12:57:36 4f21b5a Y Just using docopt now. Added option to not group git logs by any time unit (just a single list)
  Sat 2018-01-13 13:19:55 b5ead74 Z started author
  Sun 2018-01-14 18:50:28 4c1ac38 a Added options: au and fullhash
  Mon 2018-01-15 15:54:34 d6a9eca b Can now match multiple searches.
  Mon 2018-01-15 15:55:05 03b604b c rm debug prints
  Wed 2018-01-17 12:25:12 dd36ec6 d Sort data by alias or by filename
    A...E......................... AM .gitignore
    A.............................  A LICENSE
    .BC.E..H.J.L.N...R..UV..Y.a..d AM src/bin/gitlog.py
    .BC........................... AR src/gitlog_prt/gitlog.py
    .BC........................... AR src/gitlog_prt/cli.py
    .BC........................... AR src/gitlog_prt/__init__.py
    .B..E...IJK......R............ AM README.md
    ..CDEFG....L.NO.QR......Y.a..d RM src/prtgitlog/gitlog.py
    ..C.E.....KL.NOP.RS.UVWXYZabcd RM src/prtgitlog/cli.py
    ..C................T.......... RM src/prtgitlog/__init__.py
    ...DEF..I...........UV........ AM makefile
    ...DEF......M....R............ AM src/prtgitlog/prthdrs.py
    ...DEF..........QR......Y..... AM src/prtgitlog/sortbytime.py
    ...D.FG.......O.QR..U.W..Zab.. AM src/prtgitlog/data.py
    ....E...........Q............. AM .pylintrc
    .....F..I.......QR........a..d AM src/prtgitlog/prtlog.py
    ...................T..........  A setup.py
```

### Sort by filename
```
```


## Links

- [Git Commit Limiting](https://git-scm.com/docs/git-log#_commit_limiting)
- [Git Basics - Viewing the Commit History](https://git-scm.com/book/en/v1/Git-Basics-Viewing-the-Commit-History)
- [docopt blog](https://www.robjwells.com/2015/06/you-should-be-using-docopt)
- [docopt](https://github.com/docopt/docopt)
- [git: list all files added/modified on a day (or week/month)](
   https://stackoverflow.com/questions/8016645/git-list-all-files-added-modified-on-a-day-or-week-month)


Copyright (C) 2017-present, DV Klopfenstein. All rights reserved.
