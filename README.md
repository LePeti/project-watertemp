# project-watertemp

![](https://github.com/LePeti/project-watertemp/actions/workflows/workflow.yml/badge.svg)

**The goal of this project is to scrape and accumulate data on Hungarian natural water (rivers, lakes) temperatures.**

## Setup

+ Run `make` in your terminal to see and run most available commands.
+ Run `make init-githook` once at the beginning (and each time a hook is added to `/.githooks`.)
+ Run `make build`, then
+ run `make build-dev` to build the base and the development image
+ Press `cmd + shift + p` and type "reopen in container" and select the first item from the dropdown list. This will launch VSCode's '*Dev Container*'. VSC will now reload within a Docker container originated from the development image that you've just built.
  + All VSC functionalities, such as the terminal, tests, debugging, etc. will use the dev container's resources.

## Heroku

+ service name in `heroku.yml` must be `web`
+ web service dynos can be scaled down to 0 for the scheduler and on-off runs to operate
+ set your Heroku stack to 'container': `heroku stack:set container -a water-temp`
+ Inspect the env vars set on Heroku: `heroku config -a water-temp`

## CI/CD

+ On commit, the `.githooks/pre-commit` script will run `make test`. If it fails, the commit will fail too
+ On push, a Github Action CI will trigger which is configured in `.github/workflows/workflow.yml`
+ **Note**, CI will only trigger when a file listed in `.github/workflows/workflow.yml` under `paths` changes. [Source](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#onpushpull_requestpaths).
+ Github Actions is configured to test and then to push the prod and dev image to Heroku's registry, finally to deploy the prod image into production
+ Add `[skip ci]` to the commit message to skip CI (e.g. when only modifying this `README`). [Source](https://github.blog/changelog/2021-02-08-github-actions-skip-pull-request-and-push-workflows-with-skip-ci/).

## Dev. resources

### Useful Postgre (PG) CLI commands

+ `make run-psql` or `make run-psql-heroku` will start up the PG cli (run it outside of the dev docker container)
+ `\d` will list your tables
+ __SELECT__: `select * from water_temp_unique limit 10;`
+ __DELETE__: `delete from water_temp_unique where location in ('Szelidi-tó')`
