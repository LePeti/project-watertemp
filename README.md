# python-workflow

**A boilerplate python development workflow with Docker, Git, Make, automatic
testing, code formatting, codestyle check and more.**

## Setup

+ Run `make` in your terminal to see and run most available commands.
+ Run `make init-githook` once at the beginning (and each time a hook is added
  to `/.githooks`.)
+ Run `make build`, then
+ run `make build-dev` to build the base and the development image
+ Press `cmd + shift + p` and type "reopen in container" and select the first
  item from the dropdown list. This will launch VSCode's '*Dev Container*'.
  VSC will now reload within a Docker container originated from the development
  image that you've just built.
  + All VSC functionalities, such as the terminal, tests, debugging, etc. will
    use the dev container's resources.
