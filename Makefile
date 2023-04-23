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
	pip install wheel
	python setup.py sdist bdist_wheel

bump:
	if python -c "import package_name" &> /dev/null; then
		echo 'Generating changelog with commitizen and bumping the package version'
	else
		echo 'Install commitizen first with pip install commitizen==3.0.1'
	fi
	
	cz changelog
	semantic-release version

release:
	pip install twine==3.8.0
	twine upload --username __token__ --password ${PYPI_TOKEN} dist/* 
