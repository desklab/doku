FROM python:3.8-slim-buster
LABEL maintainer="j.drotleff@desk-lab.de"

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
ENV DOKU_CONFIG config.prod

ENV HEALTHCHECK_URL http://0.0.0.0:8000/api/v1/heartbeat
ENV HEALTHCHECK_HOST 0.0.0.0:8000

RUN apt-get update
RUN apt-get -y install curl build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Install fonts
RUN apt-get -y install fonts-comfortaa
ADD https://raw.githubusercontent.com/googlefonts/nunito/master/fonts/TTF/Nunito-Regular.ttf /usr/local/share/fonts/
ADD https://raw.githubusercontent.com/googlefonts/nunito/master/fonts/TTF/Nunito-Bold.ttf /usr/local/share/fonts/

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip --no-cache-dir install -r requirements.txt
RUN pip install uwsgi

RUN rm -rf ~/.cache/pip/*

COPY . /app/

RUN useradd doku
CMD mkdir /app/resources
RUN chmod +x /app/docker-entrypoint.sh
RUN chmod +x /app/healthcheck.sh
RUN chown -R doku /app

USER doku


EXPOSE 8000
WORKDIR /app

HEALTHCHECK CMD ./healthcheck.sh

CMD ./docker-entrypoint.sh
