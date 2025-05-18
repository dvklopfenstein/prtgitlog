# For editing and running gitlog scrip

PY_ALL := $(shell find src -name '[a-z0-9]*.py')

PYCODE := \
       src/bin/gitlog \
       prtgitlog/cli.py \
       prtgitlog/gitlog.py \
       prtgitlog/gitlog_strm.py \
       prtgitlog/sortbytime.py \
       prtgitlog/prtlog.py \
       prtgitlog/commit_aliases.py \
       prtgitlog/commit_info.py \
       prtgitlog/commit_files.py \
       src/tests/test_cli.py

run:
	gitlog

pylint:
	@for py in $(PY_ALL) ; do \
		echo $$py ; pylint -r no $$py ; \
	done

vim_:
	vim -p $(PYCODE)

vim_md:
	vim -p ./README.md ./doc/md/README_example_succint.md ./doc/md/README_TBD.md

g:
	git status
	git remote -v
	git branch

p:
	find src -type f -name \*.py


# = DISRIBUTION ==================================================================
pytest:
	python3 -m pytest -v src/tests | tee pytest_dv.log
	
vim_ver:
	vim -p pyproject.toml CHANGELOG.md ./prtgitlog/__init__.py

tags:
	git log --decorate=full --simplify-by-decoration --pretty=oneline HEAD
	git tag -l -n

push_tags:
	#git push --tags origin HEAD
	git push --follow-tags

# Test in a virtual environment
prep_env:
	conda remove --name myenv --all
	conda create --name myenv
# conda activate myenv
# conda install -c dvklopfenstein prtgitlog
# /usr/bin/gitlog
# conda deactivate

upload_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest


# = CLEAN ========================================================================
clean_build:
	rm -rf dist build prtgitlog.egg-info

clean:
	make -f makefile clean_dist
	find . -name \*.pyc | xargs rm -f


# Copyright (C) 2014-present, DV Klopfenstein. All rights reserved.
