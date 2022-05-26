# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

EXPOSE 5000/tcp

WORKDIR /ilp_api

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "flask", "run", "--host=0.0.0.0"]