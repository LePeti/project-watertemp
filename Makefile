.PHONY: help build shell test format clean up down app

.DEFAULT: help

help: ## Print this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

export DOCKER_BUILDKIT=1

build: ## Build based on Dockerfile and name it 'project-watertemp'
	docker build \
		-t project-watertemp \
		-f Dockerfile \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from registry.heroku.com/water-temp/web \
		.

build-dev: ## Build based on dev.Dockerfile and name it 'project-watertemp-dev'
	docker build \
		-t project-watertemp-dev \
		-f dev.Dockerfile \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from registry.heroku.com/water-temp/web-dev \
		.

heroku-login: ## logging into heroku
	heroku container:login

up: ## docker-compose up -d
	docker-compose up -d

down: ## docker-compose down
	docker-compose down

shell: ## Start a shell session in docker
	docker-compose up -d
	docker exec -ti project-watertemp-vsc-dev /usr/bin/zsh

heroku-shell: ## Start a shell in docker on Heroku
	heroku run -a water-temp bash

dockerized-test: ## Run flake8 syntax and codestyle check, then run tests with pytest, finally test dbt tables (dockerized)
	@docker run --rm \
		-v `pwd`/tests:/app/tests:rw \
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
		-v `pwd`/tests:/app/tests:rw \
		--name project-watertemp-test \
		project-watertemp-dev \
		/bin/bash -c \
			"black --line-length=90 src tests; \
			isort --profile black src tests ; \
			flake8 --max-line-length 90 src tests"

clean: ## Delete /.pytest_cache and tests/__pycache__
	rm -rf .pytest_cache **/__pycache__
	dbt clean
	# TODO: didn't clean up in functions folder

init-githook: ## Remove any symlink from .git/hooks, then symlink the /.githooks folder into .git/hooks (this way we can share git-hooks on github)
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;

scrape-on-heroku: ## Run scarping once on Heroku using a one-off dyno
	heroku run -a water-temp python -m src.main

heroku-dbt-test: ## Run dbt test on heroku
	heroku run -a water-temp dbt test

scrape-locally: ## Run scarping once locally
	python -m src.main

query-wt-raw: ## Query and print the results of the water_temp_raw table
	python -m src.dev.query_local_tables

app: ## Start dash app locally
	python -m src.dashboard.app

# The below is commented out so that no accidental deletion happens
# truncate-raw-on-heroku: ## Delete all raws (truncate) from table 'water-temp-raw' in the Heroku hosted db
# 	heroku run -a water-temp python src/dev/truncate_db.py

truncate-raw-locally: ## Delete all raws (truncate) from table 'water-temp-raw' locally
	python -m src.dev.truncate_db water_temp_raw

truncate-unique-locally: ## Delete all raws (truncate) from table 'water-temp-raw' locally
	python -m src.dev.truncate_db water_temp_unique

run-psql: ## Run PSQL to query tables locally (only run outside of devcontainer terminal)
	docker exec -it project-watertemp-pg-db bash -c "PGPASSWORD=secret psql -d postgres -U postgres"

# You can do the same on heroku's psql, just add (see vars in .env)
# -h HEROKU_PG_HOST_NAME
# Or just do

run-psql-heroku: ## Run PSQL on Heroku (only run outside of devcontainer terminal)
	heroku pg:psql postgresql-reticulated-85975 --app water-temp
