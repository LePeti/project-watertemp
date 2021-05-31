# project-watertemp

**The goal of this project is to scrape and accumulate data on Hungarian natural water (rivers, lakes) temperatures.**

![CI Build](https://github.com/LePeti/project-watertemp/actions/workflows/workflow.yml/badge.svg)
## Setup

+ Run `make` in your terminal to see and run most available commands.
+ Run `make init-githook` once at the beginning (and each time a hook is added to `/.githooks`.)
+ Run `make build`, then
+ run `make build-dev` to build the base and the development image
+ Press `cmd + shift + p` and type "reopen in container" and select the first item from the dropdown list. This will launch VSCode's '*Dev Container*'. VSC will now reload within a Docker container originated from the development image that you've just built.
  + All VSC functionalities, such as the terminal, tests, debugging, etc. will use the dev container's resources.

## Heroku

+ service name in `heroku.yml` must be web
+ web service dynos can be scaled down to 0 for the scheduler and on-off runs to operate
+ set your Heroku stack to 'container': `heroku stack:set container -a water-temp`
+ Inspect the env vars set on Heroku: `heroku config -a water-temp`
