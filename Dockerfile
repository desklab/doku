FROM python:3.8-slim-buster
LABEL maintainer="j.drotleff@desk-lab.de"

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
ENV DOKU_CONFIG config.prod

# Install Node.js
RUN apt-get update
RUN apt-get -y install curl gnupg build-essential
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get -y install nodejs

# Verify Node.js
RUN node -v
RUN npm -v

COPY ./doku/static/package-lock.json /app/doku/static/package-lock.json
COPY ./doku/static/package.json /app/doku/static/package.json

WORKDIR /app/doku/static
COPY ./doku/static/ /app/doku/static/
RUN npm ci
RUN npm rebuild node-sass --unsafe-perm
RUN npm run build
RUN rm -rf node_modules

RUN apt-get clean
RUN apt-get remove -y --purge curl gnupg nodejs build-essential

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip --no-cache-dir install -r requirements.txt

RUN rm -rf ~/.cache/pip/*

COPY . /app/

RUN useradd doku
RUN chown -R doku /app

USER doku

EXPOSE 8000
WORKDIR /app
CMD /docker-entrypoint.sh
