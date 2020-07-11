FROM python:3.7.7-stretch

WORKDIR /restfulAPI

ADD . /restfulAPI

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install software-properties-common

RUN add-apt-repository universe

RUN add-apt-repository ppa:certbot/certbot

RUN apt-get update

RUN apt-get install certbot python3-certbot-nginx

RUN certbot -d pttlite.ddns.net

RUN certbot --nginx

CMD ["uwsgi", "uwsgi.ini"]