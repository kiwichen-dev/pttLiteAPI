FROM nginx

# FROM ubuntu:18.04

RUN apt-get update

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

COPY blacklist.conf /etc/nginx/

EXPOSE 443