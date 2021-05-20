.PHONY: help build shell test format clean up down

.DEFAULT: help

ifneq ($(findstring .env,$(wildcard .env)), )
    include .env
endif

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build based on Dockerfile and name it 'project-watertemp'
	docker build -t project-watertemp -f Dockerfile .

build-dev: ## Build based on dev.Dockerfile and name it 'project-watertemp-dev'
	docker build -t project-watertemp-dev -f dev.Dockerfile .

up: ## docker-compose up -d
	docker-compose up -d

down: ## docker-compose down
	docker-compose down

shell: ## Start a shell session in docker
	docker-compose up -d
	docker exec -ti project-watertemp-vsc-dev /usr/bin/zsh

dockerized-test: ## Run flake8 syntax and codestyle check, then run tests with pytest , finally test dbt tables (dockerized)
	@docker run --rm \
		-v `pwd`/:/app:rw \
		--name project-watertemp-test \
		project-watertemp-dev \
		/bin/bash -c \
			"flake8 --max-line-length 90 src tests; \
			pytest tests"

test: ## Run flake8 syntax and codestyle check, then run tests with pytest , finally test dbt tables
	flake8 --max-line-length 90 src tests
	pytest tests
	make clean

format: ## Run flake8 syntax and codestyle check, then run tests with pytest
	black --line-length=90 src tests
	isort --profile black src tests
	flake8 --max-line-length 90 src tests

dockerized-format: ## Format code with black, then run codestyle checks (dockerized)
	docker run --rm \
		-v `pwd`/:/app:rw \
		--name project-watertemp-test \
		project-watertemp-dev \
		/bin/bash -c \
			"black --line-length=90 src tests; \
			isort --profile black src tests ; \
			flake8 --max-line-length 90 src tests"

clean: ## Delete /.pytest_cache and tests/__pycache__
	rm -rf .pytest_cache **/__pycache__
	dbt clean
	# FIX: didn't clean up in functions folder

init-githook: ## Remove any symlink from .git/hooks, then symlink the /.githooks folder into .git/hooks (this way we can share git-hooks on github)
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;

scrape-on-heroku: ## Run scarping once on Heroku using a one-off dyno
	heroku run -a water-temp python -m src.main

scrape-locally: ## Run scarping once locally
	python -m src.main

# The below is commented out so that no accidental deletion happens
# truncate-raw-on-heroku: ## Delete all raws (truncate) from table 'water-temp-raw' in the Heroku hosted db
# 	heroku run -a water-temp python src/dev/truncate_db.py

truncate-raw-locally: ## Delete all raws (truncate) from table 'water-temp-raw' locally
	python -m src.dev.truncate_db water_temp_raw

truncate-unique-locally: ## Delete all raws (truncate) from table 'water-temp-raw' locally
	python -m src.dev.truncate_db water_temp_unique
