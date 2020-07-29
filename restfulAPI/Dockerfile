FROM ubuntu:18.04

# FROM python:3.7.7-stretch

WORKDIR /restfulAPI

ADD . /restfulAPI

# RUN cat /etc/os-release

RUN apt-get install python3

RUN pip install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]