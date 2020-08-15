# SCRIPT: Call _git log_ through the gitlog script
  * Commit information is listed in the header paragraph and shows the commit hash (e.g., 5c791c3)    
  * Each commit is given an alias (e.g., A B C D E F G)    
  * Files commited are listed below the header paragraph (e.g., src/prtgitlog/commit_info.py)     

```
$ gitlog --after="2 days"

  Thu 2018-01-25 13:19:03 5c791c3 A Use weekday number instead of letter
  Fri 2018-01-26 14:27:17 8e3301a B Now passing 'git log' options: after before since until
  Fri 2018-01-26 15:09:15 ee21efb C Added outline for more examples
  Fri 2018-01-26 15:12:26 cd7bbd8 D fmt
  Fri 2018-01-26 15:13:12 0499d1a E fmt
  Fri 2018-01-26 15:14:59 e722048 F bold accent
  Fri 2018-01-26 15:16:14 d2c04f4 G codeblock
    AB..... M src/prtgitlog/commit_info.py
    .BCDEFG M README.md
    .B..... M src/prtgitlog/cli.py
```

Copyright (C) 2017-present, DV Klopfenstein. All rights reserved.
