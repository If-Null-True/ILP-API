# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

EXPOSE 5000

WORKDIR /ilp_api

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-b" ,":5000", "--access-logfile",  "-", "--error-logfile", "-", "--workers", "3", "wsgi:app"]