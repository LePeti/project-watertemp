.PHONY: help build shell test format clean

.DEFAULT: help

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build based on Dockerfile and name it 'project-watertemp'
	docker build -t project-watertemp -f Dockerfile .

build-dev: ## Build based on Dockerfile-dev and name it 'project-watertemp-dev'
	docker build -t project-watertemp-dev -f Dockerfile-dev .

up: ## docker-compose up -d
	docker-compose up -d

down: ## docker-compose down
	docker-compose down

shell:
	docker-compose up -d
	docker exec -ti project-watertemp-vsc-dev /usr/bin/zsh

dockerized-test: ## Run flake8 syntax and codestyle check, then run tests with pytest (dockerized)
	docker run --rm \
		-v `pwd`/:/app:rw \
		--name project-watertemp-test \
		project-watertemp-dev \
		/bin/bash -c \
			"flake8 --max-line-length 90 src tests; \
			pytest"

test: ## Run flake8 syntax and codestyle check, then run tests with pytest
	flake8 --max-line-length 90 src tests
	pytest
	make clean

format: ## Run flake8 syntax and codestyle check, then run tests with pytest
	black --line-length=90 src tests
	isort --profile black .
	flake8 --max-line-length 90 src tests

dockerized-format: ## Format code with black, then run codestyle checks (dockerized)
	docker run --rm \
		-v `pwd`/:/app:rw \
		--name project-watertemp-test \
		project-watertemp-dev \
		/bin/bash -c \
			"black --line-length=90 src tests; \
			isort --profile black . ; \
			flake8 --max-line-length 90 src tests"

clean: ## Delete /.pytest_cache and tests/__pycache__
	rm -rf .pytest_cache **/__pycache__

init-githook: ## Remove any symlink from .git/hooks, then symlink the /.githooks folder into .git/hooks (this way we can share git-hooks on github)
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;
