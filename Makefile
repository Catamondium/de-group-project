#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = de-py-katas
REGION = eu-west-2
PYTHON_INTERPRETER = python3
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip
PYTEST_OPTS = -vvvv
PYTEST_COV = --cov=src --cov-fail-under=90 --no-cov-on-fail --cov-report=term-missing
PYTHONPATH=./src
TRACK=make_trackers
VENV=venv
SITE_PACKAGES=$(VENV)/lib/*/site-packages/

## Run all checks
run-checks: run-security run-flake unit-tests

## Create python interpreter environment.
$(VENV):
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    $(PYTHON_INTERPRETER) -m venv $(VENV); \
	)

$(SITE_PACKAGES) $(TRACK)/packages : requirements.txt
	$(call execute_in_env, $(PIP) install -r requirements.txt)
	touch $(TRACK)/packages

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

################################################################################################################
# Set Up
## local testing database
init-db:
	# Why does make have to parse like this?
	if [[ ! -f .env.ini ]]; then \
		echo -e "[DEFAULT]\nPGUSER=\nPGPASSWORD=\n" > .env.ini; \
	fi;
	psql -f ./test/test_extract_db/subset_test_db.sql

## Install flake8
dev-setup: requirements init-db
	$(call execute_in_env, $(PIP) install flake8)
	$(call execute_in_env, $(PIP) install pytest)
	$(call execute_in_env, $(PIP) install bandit)
	$(call execute_in_env, $(PIP) install safety)
	$(call execute_in_env, $(PIP) freeze > requirements.txt)
	ln -sf $(realpath pre-commit.sh) .git/hooks/pre-commit


## Run the flake8 code check
run-flake:
	$(call execute_in_env, flake8 src test)

run-bandit:
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

$(TRACK)/safety : requirements.txt
	$(call execute_in_env, safety check -r ./requirements.txt)
	touch $(TRACK)/safety

## Run all the unit tests
unit-tests:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest ${PYTEST_OPTS} ${PYTEST_COV} test/*.py)

run-security: run-bandit $(TRACK)/safety

init: create-environment requirements init-db