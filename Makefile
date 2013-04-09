.PHONY: docs build test coverage pylint flake8 pep8 pyflakes templer diff sloccount dryrelease mkrelease

ifndef VTENV_OPTS
VTENV_OPTS = "--no-site-packages"
endif

docs: bin/sphinx-build
	SPHINXBUILD=../bin/sphinx-build $(MAKE) -C docs html $^

build:	
	virtualenv $(VTENV_OPTS) .
	bin/python setup.py develop

test: bin/nosetests
	bin/nosetests -s encode/human

coverage: bin/coverage bin/nosetests
	bin/nosetests --with-coverage --cover-html --cover-html-dir=html --cover-package=encode.human
	bin/coverage html

pylint:	bin/pylint
	bin/pylint -i y encode/human

flake8:	bin/flake8
	bin/flake8 --max-complexity 12 encode/human

pep8:	bin/pep8
	bin/pep8 encode/human

pyflakes:	bin/pyflakes
	bin/pyflakes encode/human

templer: bin/python
	# Hack to make believe templer that the current folder is the home folder
	# so that it reads the local .zopeskel file with the defaults
	export OLDHOME="${HOME}"; export HOME="${PWD}"; ./bin/templer dotpackage encode.human; export HOME="${OLDHOME}"

diff: bin/python
	# Show the difference between the current package and the regenerated one
	colordiff -c -r encode.human .|less -r

sloccount:	bin/python
	sloccount encode/human

dryrelease:	bin/mkrelease
	bin/mkrelease --no-commit --no-tag --dry-run -d pypi

mkrelease:	bin/mkrelease
	bin/mkrelease --no-commit --no-tag  -d pypi

bin/sphinx-build: bin/python
	bin/pip install sphinx
	bin/pip install coverage

bin/nosetests: bin/python
	bin/pip install nose

bin/coverage: bin/python
	bin/pip install coverage

bin/pylint: bin/python
	bin/pip install pylint

bin/flake8: bin/python
	bin/pip install flake8

bin/pyflakes: bin/python
	bin/pip install pyflakes

bin/pep8: bin/python
	bin/pip install pep8

bin/mkrelease: bin/python
	bin/pip install jarn.mkrelease
