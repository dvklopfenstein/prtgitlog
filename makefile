# For editing and running gitlog scrip

PYCODE := \
	src/bin/gitlog.py \
	src/prtgitlog/cli.py \
	src/prtgitlog/gitlog.py \
	src/prtgitlog/data.py \
	src/prtgitlog/sortbytime.py \
	src/prtgitlog/prtlog.py \
	src/prtgitlog/prthdrs.py

run:
	gitlog

pylint:
	@for py in $(PYCODE) ; do \
		echo $$py ; pylint -r no $$py ; \
	done

vim_:
	vim -p $(PYCODE)

clean:
	find . -name \*.pyc | xargs rm -f


# Copyright (C) 2014-2017, DV Klopfenstein. All rights reserved.
