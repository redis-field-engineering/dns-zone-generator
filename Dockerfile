FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev git zlib1g-dev libjpeg-dev libfreetype6-dev supervisor

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /etc/supervisor/conf.d

RUN apt-get install -y redis-server

COPY ./requirements.txt /app/requirements.txt

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf" ]
