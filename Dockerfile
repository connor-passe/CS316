FROM python:3.8

RUN pip install Flask
RUN mkdir /app

ADD . /app
