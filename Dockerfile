FROM python:3.13-alpine3.22

COPY requirements.txt /temp/requirements.txt
COPY service /service

WORKDIR /service

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
