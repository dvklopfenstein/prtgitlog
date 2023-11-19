# For editing and running gitlog scrip

PY_ALL := $(shell find src -name '[a-z0-9]*.py')

PYCODE := \
       src/bin/gitlog \
       src/prtgitlog/cli.py \
       src/prtgitlog/gitlog.py \
       src/prtgitlog/gitlog_strm.py \
       src/prtgitlog/sortbytime.py \
       src/prtgitlog/prtlog.py \
       src/prtgitlog/commit_aliases.py \
       src/prtgitlog/commit_info.py \
       src/prtgitlog/commit_files.py \
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
	vim -p CHANGELOG.md ./src/prtgitlog/__init__.py setup.py makefile

build:
	# python3 -m pip install --user --upgrade setuptools wheel
	make clean_dist
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	ls -lh dist
	twine check dist/*

# Use conda build to build pkgs for Python to install rather than conda
bdist_conda:
	# Allow installation from the conda-forge channel to install neobolt
	# conda config --add channels defaults
	# conda config --add channels bioconda
	# conda config --add channels conda-forge
	# # Use the neo4j-python-driver from conda-forge
	# conda config --set channel_priority strict
	python setup.py bdist_conda
	# anaconda login
	# anaconda upload /home/neo4j/anaconda3/conda-bld/linux-64/prtgitlog-0.1.VER-py36_0.tar.bz2
	# anaconda logout

upload_pip:
	python3 -m twine upload dist/* --verbose

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
clean_dist:
	rm -rf dist build prtgitlog.egg-info

clean:
	make -f makefile clean_dist
	find . -name \*.pyc | xargs rm -f


# Copyright (C) 2014-present, DV Klopfenstein. All rights reserved.
