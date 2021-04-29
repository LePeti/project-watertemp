FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        libpq-dev \
        gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm -rf requirements.txt

COPY src src
