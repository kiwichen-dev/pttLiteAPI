FROM python:3.7.7-stretch

WORKDIR /restfulAPI

ADD . /restfulAPI

RUN pip install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]