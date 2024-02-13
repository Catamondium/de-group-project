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
PYTHONPATH=./src

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    $(PYTHON_INTERPRETER) -m venv venv; \
	)

requirements: venv requirements.txt
	$(call execute_in_env, $(PIP) install -r requirements.txt)
	ln -sf $(realpath pre-commit.sh) .git/hooks/pre-commit


# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

################################################################################################################
# Set Up
## Install flake8
flake:
	$(call execute_in_env, $(PIP) install flake8)

## Install pytest
pytest:
	$(call execute_in_env, $(PIP) install pytest)

## Install pytest
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install pytest
safety:
	$(call execute_in_env, $(PIP) install safety)

dev-setup: bandit safety pytest flake requirements

## Run the flake8 code check
run-flake:
	$(call execute_in_env, flake8 src test)

run-bandit:
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

run-safety: requirements.txt
	$(call execute_in_env, safety check -r ./requirements.txt)

## Run all the unit tests
unit-tests:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest ${PYTEST_OPTS} test/*.py)

run-security: run-bandit run-safety

## Run all checks
run-checks: run-security run-flake unit-tests