# syntax=docker/dockerfile:1

FROM python:3.12.8-bookworm

WORKDIR /app
COPY . /app
RUN pip3 install -r ./requirements.txt
EXPOSE 8080
CMD python ./app.py
