# For editing and running gitlog scrip

PY_ALL := $(shell find src -name '[a-z0-9]*.py')

PYCODE := \
       src/bin/gitlog.py \
       src/prtgitlog/cli.py \
       src/prtgitlog/gitlog.py \
       src/prtgitlog/gitlog_strm.py \
       src/prtgitlog/sortbytime.py \
       src/prtgitlog/prtlog.py \
       src/prtgitlog/commit_aliases.py \
       src/tests/test_cli.py

run:
	gitlog

pylint:
	@for py in $(PY_ALL) ; do \
		echo $$py ; pylint -r no $$py ; \
	done

pytest:
	python -m pytest src/tests/

vim_:
	vim -p $(PYCODE)

clean:
	find . -name \*.pyc | xargs rm -f


# Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved.
