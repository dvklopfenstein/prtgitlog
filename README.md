# gitlog
Print **_git log_** output in a **succinct** format **grouped** by day, week, month, year, or ungrouped(all)    

For help for the gitlog script, do either:
```
$ gitlog --help
$ gitlog.py --help
```

## Succinct Output: Comparison

| Description           | # Lines | Example Output
|-----------------------|---------|-------------------------
| _git log_ COMMAND     |      71 | [git log --after "2 days"](doc/md/README_example_succint.md#cmdline-call-git-log-from-the-command-line)
| _gitlog_ REPO SCRIPT  |      18 | [gitlog --after="2 days"](doc/md/README_example_succint.md#script-call-git-log-through-the-gitlog-script)


## Links

- [Git Basics - Viewing the Commit History](https://git-scm.com/book/en/v1/Git-Basics-Viewing-the-Commit-History)
- [docopt blog](https://www.robjwells.com/2015/06/you-should-be-using-docopt)
- [docopt](https://github.com/docopt/docopt)
- [git: list all files added/modified on a day (or week/month)](
   https://stackoverflow.com/questions/8016645/git-list-all-files-added-modified-on-a-day-or-week-month)

Copyright (C) 2017-2018, DV Klopfenstein. All rights reserved.
