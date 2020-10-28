FROM nginx

RUN apt-get update \
    && apt upgrade \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/ \
    && blacklist.conf /etc/nginx/

EXPOSE 443