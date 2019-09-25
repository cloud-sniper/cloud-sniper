ARG BASE_CONTAINER=python:3

FROM $BASE_CONTAINER

FROM python:3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install awscli

COPY aws_credentials.txt /root/.aws/credentials

WORKDIR /usr/src/beaconer

COPY entrypoint.sh ./
COPY environment.env ./
COPY ./src/* ./

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
