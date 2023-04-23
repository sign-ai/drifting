.ONESHELL:

CMD = python

PACKAGE_DIR = drifting
TEST_DIR = tests

.PHONY = help setup test run clean

help:
	@echo "---------------HELP-----------------"
	@echo "Run make _command_. See Makefile for "
	@echo "the reference."
	@echo "------------------------------------"

install-poetry:
	pip install poetry==1.1.14
	
install-prod:
	poetry install

install:
	# poetry install --with dev,test
	pip install -r requirements.txt

test:
	${CMD} -m pytest tests/

check-all:
	${CMD} -m black --check ${PACKAGE_DIR} ${TEST_DIR}
	${CMD} -m pylint ${PACKAGE_DIR} ${TEST_DIR}
	${CMD} -m mypy --ignore-missing-imports ${PACKAGE_DIR} ${TEST_DIR}
	
format:
	${CMD} -m black ${PACKAGE_DIR} ${TEST_DIR}

build:
	python setup.py sdist bdist_wheel

bump:
	semantic-release version
	semantic-release changelog > CHANGELOG.md

release:
	pip install twine==3.8.0
	twine upload --username __token__ --password ${PYPI_TOKEN} dist/* 
