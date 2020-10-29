FROM nginx

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install certbot python-certbot-nginx -y \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

COPY blacklist.conf /etc/nginx/