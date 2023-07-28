SHELL := /bin/bash
# =============================================================================
# Variables
# =============================================================================

.DEFAULT_GOAL:=help
.ONESHELL:
USING_POETRY	=	$(shell grep "tool.poetry" pyproject.toml && echo "yes")
ENV_PREFIX		=	$(shell python3 -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
VENV_EXISTS		=	$(shell python3 -c "if __import__('pathlib').Path('.venv/bin/activate').exists(): print('yes')")
REPO_INFO 		?= 	$(shell git config --get remote.origin.url)
COMMIT_SHA 		?= 	git-$(shell git rev-parse --short HEAD)
POETRY_OPTS 	?=
POETRY 			?= 	poetry $(POETRY_OPTS)
POETRY_RUN_BIN 	= 	$(POETRY) run
SPHINXBUILD 	=	sphinx-build
SPHINXAUTOBUILD = 	sphinx-autobuild

.EXPORT_ALL_VARIABLES:

.PHONY: help upgrade install-poetry set-up-poetry install-pre-commit install
.PHONY: fmt-fix test coverage check-all lint fmt-check
.PHONY: docs-install docs-clean docs-serve docs-build
.PHONY: clean run-dev-frontend run-dev-server production develop destroy

help: ## Display this help text for Makefile
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

upgrade:       ## Upgrade all dependencies to the latest stable versions
	@if [ "$(USING_POETRY)" ]; then $(POETRY) update; fi
	@echo "Dependencies Updated"

# =============================================================================
# Developer Utils
# =============================================================================

install-poetry: ## Install latest version of poetry
	@echo "Installing poetry..."
	@curl -sSL https://install.python-poetry.org | python3 -
	@`eval include ${HOME}/.poetry/env`

set-up-poetry: ## Set up poetry
	@poetry env use python3 && $(POETRY) install --with dev

install-pre-commit: ## Install pre-commit and install hooks
	@echo "Installing pre-commit"
	@pip3.11 install pre-commit==3.2.0
	@pre-commit install --install-hooks --all
	@pre-commit install --hook-type commit-msg
	@echo "pre-commit installed"

install: ## Install all dependencies
	@echo "Installing..."
	@command -v $(POETRY) > /dev/null || (echo "Poetry not found. Installing..." && $(MAKE) install-poetry)
	$(MAKE) set-up-poetry
	$(MAKE) install-pre-commit

# =============================================================================
# Tests, Linting, Coverage
# =============================================================================

lint: ## Runs pre-commit hooks; includes ruff linting, codespell, black
	$(POETRY_RUN_BIN) pre-commit run --all-files

fmt-check: ## Runs black in check mode (no changes)
	$(POETRY_RUN_BIN) black --check --fast .

fmt-fix: ## Runs black, makes changes where necessary
	$(POETRY_RUN_BIN) black --line-length 120 .

test:  ## Run the tests
	$(POETRY_RUN_BIN) pytest tests

coverage:  ## Run the tests and generate coverage report
	$(POETRY_RUN_BIN) pytest tests --cov=app
	$(POETRY_RUN_BIN) coverage html
	$(POETRY_RUN_BIN) coverage xml

check-all: lint test fmt-check coverage ## Run all linting, tests, and coverage checks

# =============================================================================
# Docs
# =============================================================================

docs-install: ## Install docs dependencies
	$(POETRY) env use python3 && $(POETRY) install --with dev,docs

docs-clean: ## Dump the existing built docs
	rm -rf docs/_build

docs-serve: docs-clean ## Serve the docs locally
	$(POETRY_RUN_BIN) $(SPHINXAUTOBUILD) docs docs/_build/ -j auto --watch app --watch docs --watch tests --watch CONTRIBUTING.rst --port 8002

docs: docs-clean ## Dump the existing built docs and rebuild them
	$(POETRY_RUN_BIN) $(SPHINXBUILD) -M html docs docs/_build/ -E -a -j auto --keep-going

# =============================================================================
# Main
# =============================================================================

clean: ## Autogenerated File Cleanup
	rm -rf .scannerwork/
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .hypothesis
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.ipynb_checkpoints' -exec rm -rf {} +
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf coverage.json
	rm -rf htmlcov/
	rm -rf .pytest_cache
	rm -rf tests/.pytest_cache
	rm -rf tests/**/.pytest_cache
	rm -rf .mypy_cache
	find tools/downloads -type f -delete
	$(MAKE) docs-clean

destroy: ## Destroy the virtual environment
	rm -rf .venv

develop: install ## Install the project in dev mode.
	@if ! $(POETRY) --version > /dev/null; then echo 'poetry is required, installing...'; $(MAKE) install-poetry; fi
	@if [ "$(VENV_EXISTS)" ]; then echo "Removing existing virtual environment"; fi
	if [ "$(VENV_EXISTS)" ]; then $(MAKE) destroy; fi
	if [ "$(VENV_EXISTS)" ]; then $(MAKE) clean; fi
	if [ "$(USING_POETRY)" ]; then $(POETRY) config virtualenvs.in-project true  && $(POETRY) config virtualenvs.options.always-copy true && python3 -m venv --copies .venv && source .venv/bin/activate && .venv/bin/pip install -U wheel setuptools cython pip && $(POETRY) install --with dev,lint,docs; fi
	if [ "$(VENV_EXISTS)" ]; then cp .env.example .env; fi
	@echo "=> Install complete! Note: If you want to re-install re-run 'make develop'"

production:	 ## Install the project in production mode.
	@if ! $(POETRY) --version > /dev/null; then echo 'poetry is required, installing..'; $(MAKE) install-poetry; fi
	@if [ "$(VENV_EXISTS)" ]; then echo "Removing existing environment"; fi
	if [ "$(VENV_EXISTS)" ]; then $(MAKE) destroy; fi
	if [ "$(USING_POETRY)" ]; then $(POETRY) config virtualenvs.in-project true  && $(POETRY) config virtualenvs.options.always-copy true && python3 -m venv --copies .venv && source .venv/bin/activate && .venv/bin/pip install -U wheel setuptools cython pip && $(POETRY) install --only main && $(POETRY) install --only docs; fi
	if [ "$(VENV_EXISTS)" ]; then cp /data/packages/tailwind/tailwindcss-3.3.1-linux-x64 .venv/bin/tailwindcss; fi
	if [ "$(VENV_EXISTS)" ]; then .venv/bin/tailwindcss -i app/domain/web/resources/input.css -o app/domain/web/resources/style.css; fi
	@echo "=> Install complete! Note: If you want to re-install re-run 'make production'"

run-dev-server: ## Run the app in dev mode
	$(POETRY_RUN_BIN) app run server --http-workers 1 --reload

run-dev-frontend: ## Run the app frontend in dev mode
	$(POETRY_RUN_BIN) tailwindcss -i app/domain/web/resources/input.css -o app/domain/web/resources/style.css --watch
