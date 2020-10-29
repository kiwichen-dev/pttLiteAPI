FROM python:3.8.6

WORKDIR /restfulAPI

ADD . /restfulAPI

RUN apt-get update \
     && apt-get upgrade -y\
     && pip install --upgrade pip \
     && pip install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]