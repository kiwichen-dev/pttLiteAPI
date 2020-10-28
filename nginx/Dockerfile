FROM nginx

RUN apt-get update \
    && apt upgrade -y \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

COPY blacklist.conf /etc/nginx/

EXPOSE 443