FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm -rf requirements.txt

ENV DBT_PROFILES_DIR /app/dbt

COPY dbt_project.yml dbt_project.yml
COPY dbt dbt
COPY src src

CMD python -m src.dashboard.app
