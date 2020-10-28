# FROM ubuntu:18.04

FROM python

WORKDIR /restfulAPI

ADD . /restfulAPI

# RUN cat /etc/os-release

RUN apt-get update \
     && apt-get install python3 -y --assume-yes apt-utils \
     && apt-get install python3-pip -y --assume-yes apt-utils \
     && apt-get install ipython3 -y --assume-yes apt-utils \
     && pip3 install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]