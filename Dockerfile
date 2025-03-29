FROM python:3.12-slim-bookworm


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev gcc curl ca-certificates python3-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /app

COPY uv.lock pyproject.toml ./
RUN uv sync
RUN rm uv.lock pyproject.toml

ENV DBT_PROFILES_DIR /app/dbt

COPY dbt_project.yml dbt_project.yml
COPY dbt dbt
COPY src src

CMD python -m src.dashboard.app
