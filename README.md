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


## CI/CD

+ On commit, the `.githooks/pre-commit` script will run `make test`. If it fails, the commit will fail too
+ On push, a Github Action CI will trigger which is configured in `.github/workflows/workflow.yml`
+ **Note**, CI will only trigger when a file listed in `.github/workflows/workflow.yml` under `paths` changes. [Source](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#onpushpull_requestpaths).
+ Github Actions is configured to test and then to push the prod and dev image to Heroku's registry, finally to deploy the prod image into production
+ Add `[skip ci]` to the commit message to skip CI (e.g. when only modifying this `README`). [Source](https://github.blog/changelog/2021-02-08-github-actions-skip-pull-request-and-push-workflows-with-skip-ci/).

## Dev. resources

### Useful Postgres (PG) CLI commands

+ `make run-psql` or `make run-psql-heroku` will start up the PG cli (run it outside of the dev docker container)
+ `\d` will list your tables
+ __SELECT__: `select * from water_temp_unique limit 10;`
+ __DELETE__: `delete from water_temp_unique where location in ('Szelidi-tó')`

### dbt

+ To set up dbt, before you first run `dbt run`, you need to remove the `pre_hook` from `dbt/models/ops/table_stats.sql` as that pre-hook tries to run the `analyze` command on the table created by that model too, which won't exist before the first `dbt run`.


### GCP Infrastructure

## Setting up GitHub Actions authentication

_I've ran the following GCP cli commands:_

1. Created a workload identity pool

```
gcloud iam workload-identity-pools create github-pool \
  --location="global" \
  --display-name="GitHub Pool"
```

Get its name:
```
gcloud iam workload-identity-pools describe github-pool \
  --location="global" \
  --format="value(name)"
```

> output: `projects/576787685789/locations/global/workloadIdentityPools/github-pool`

2. Create a OIDC provider:

```
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository_owner == 'LePeti'"
```

3. Add policy binding that enables uploading docker files to the GCP Artifact registry

```
gcloud projects add-iam-policy-binding "water-temp-dash" \
  --member="principalSet://iam.googleapis.com/projects/576787685789/locations/global/workloadIdentityPools/github-pool/attribute.repository/LePeti/project-watertemp" \
  --role="roles/artifactregistry.writer"
```
