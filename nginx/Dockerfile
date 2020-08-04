# FROM nginx

FROM ubuntu:18.04

RUN apt-get update -y \
    && apt-get install nginx -y
#   && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 443