FROM debian:stretch-slim

MAINTAINER Phillip Bailey <phillip@bailey.st>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get dist-upgrade && apt-get install -y \
    uwsgi-plugin-python \
    software-properties-common \
    nginx supervisor \
    && add-apt-repository ppa:deadsnakes/ppa  \
    && apt-get update \
    && apt-get install python3.8

COPY nginx/flask.conf /etc/nginx/sites-available/
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY app /var/www/app

RUN mkdir -p /var/log/nginx/app /var/log/uwsgi/app /var/log/supervisor \
    && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && pip3 install scikit-build \
    && pip3 install opencv-python \
    &&  pip3 install -r /var/www/app/requirements.txt \
    && chown -R www-data:www-data /var/www/app \
    && chown -R www-data:www-data /var/log 






CMD ["/usr/bin/supervisord"]
