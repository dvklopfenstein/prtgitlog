# gitlog
A script to print **_git log_** output in a **succinct** format **grouped** by day, week, month, year, or ungrouped(all)    

## Succinct Output: A Comparison

| Description           | # Lines | Example Output Codeblock
|-----------------------|---------|-------------------------
| _git log_ COMMAND     |      70 | [git log --after "2 days"](doc/md/README_example_succint_cmdline.md)
| _gitlog_ REPO SCRIPT  |      10 | [gitlog --after="2 days"](doc/md/README_example_succint_script.md)

## Grouping
**Group** by day, week, month, year, or ungrouped (all)     
```
$ gitlog --week
$ gitlog --month
$ gitlog --year
$ gitlog --day
$ gitlog --all
```

## Script Help

For help for the gitlog script, do one of:
```
$ gitlog --help
$ gitlog.py --help
$ scr/bin/gitlog.py --help
```

## Links

- [Git Commit Limiting](https://git-scm.com/docs/git-log#_commit_limiting)
- [Git Basics - Viewing the Commit History](https://git-scm.com/book/en/v1/Git-Basics-Viewing-the-Commit-History)
- [docopt blog](https://www.robjwells.com/2015/06/you-should-be-using-docopt)
- [docopt](https://github.com/docopt/docopt)
- [git: list all files added/modified on a day (or week/month)](
   https://stackoverflow.com/questions/8016645/git-list-all-files-added-modified-on-a-day-or-week-month)

Copyright (C) 2017-2019, DV Klopfenstein. All rights reserved.
