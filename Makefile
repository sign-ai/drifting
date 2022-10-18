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
	poetry install --no-dev

install:
	poetry install

test:
	${CMD} -m pytest tests/

check-all:
	${CMD} -m black --check ${PACKAGE_DIR} ${TEST_DIR}
	${CMD} -m pylint ${PACKAGE_DIR} ${TEST_DIR}
	${CMD} -m mypy --ignore-missing-imports ${PACKAGE_DIR} ${TEST_DIR}
	
format:
	${CMD} -m black ${PACKAGE_DIR} ${TEST_DIR}

build:
	rm -rf dist
	poetry build

release:
	semantic-release publish
