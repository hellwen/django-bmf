FROM python:2.7.11

ENV DOCKER 1
ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install -r requirements.txt django-debug-toolbar
