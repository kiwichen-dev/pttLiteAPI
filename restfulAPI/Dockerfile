# FROM ubuntu:18.04

FROM python:3.8.6

WORKDIR /restfulAPI

ADD . /restfulAPI

# RUN cat /etc/os-release

# RUN apt-get update \
#      && apt-get install python3 -y --assume-yes apt-utils \
#      && apt-get install python3-pip -y --assume-yes apt-utils \
#      && apt-get install ipython3 -y --assume-yes apt-utils \
#      && pip3 install -r requirements.txt

RUN apt-get update \
     && apt-get upgrade -y\
     && pip install --upgrade pip \
     && pip install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]