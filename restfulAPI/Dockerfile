FROM python:3.7.7-stretch

WORKDIR /flask

ADD . /flask

RUN pip install -r requirements.txt

CMD ["uwsgi", "uwsgi.ini"]