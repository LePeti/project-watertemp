.PHONY: help build shell test format clean

.DEFAULT: help

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build based on Docker/Dockerfile and name it 'python-workflow'
	docker build -t python-workflow -f Docker/Dockerfile .

build-dev: ## Build based on Docker/Dockerfile-dev and name it 'python-workflow-dev'
	docker build -t python-workflow-dev -f Docker/Dockerfile-dev .

shell: ## Start a development shell in docker with source code and tests mounted
	docker run --rm -it\
		-v `pwd`/:/app:rw \
		--name python-workflow-shell \
		python-workflow-dev \
		/usr/bin/zsh

dockerized-test: ## Run flake8 syntax and codestyle check, then run tests with pytest (dockerized)
	docker run --rm \
		-v `pwd`/:/app:rw \
		--name python-workflow-test \
		python-workflow-dev \
		/bin/bash -c \
			"flake8 src tests; \
			pytest"

test: ## Run flake8 syntax and codestyle check, then run tests with pytest
	flake8 src
	flake8 tests
	pytest
	make clean

format: ## Run flake8 syntax and codestyle check, then run tests with pytest
	black src tests
	flake8 src tests

dockerized-format: ## Format code with black, then run codestyle checks (dockerized)
	docker run --rm \
		-v `pwd`/:/app:rw \
		--name python-workflow-test \
		python-workflow-dev \
		/bin/bash -c \
			"black src tests; \
			flake8 src tests"

clean: ## Delete /.pytest_cache and tests/__pycache__
	rm -rf .pytest_cache **/__pycache__

init-githook: ## Remove any symlink from .git/hooks, then symlink the /.githooks folder into .git/hooks (this way we can share git-hooks on github)
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;
