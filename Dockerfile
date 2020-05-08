FROM python:3.8-slim-buster
LABEL maintainer="j.drotleff@desk-lab.de"

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
ENV DOKU_CONFIG config.prod

# Install Node.js
RUN apt-get update
RUN apt-get -y install curl gnupg build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
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
RUN apt-get remove -y --purge curl gnupg nodejs

# Install fonts
RUN apt-get -y install fonts-comfortaa
ADD https://raw.githubusercontent.com/googlefonts/nunito/master/fonts/TTF/Nunito-Regular.ttf /usr/local/share/fonts/
ADD https://raw.githubusercontent.com/googlefonts/nunito/master/fonts/TTF/Nunito-Bold.ttf /usr/local/share/fonts/ 

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip --no-cache-dir install -r requirements.txt
RUN pip install gunicorn

RUN rm -rf ~/.cache/pip/*

COPY . /app/

RUN useradd doku
RUN chown -R doku /app

USER doku

EXPOSE 8000
WORKDIR /app
CMD ./docker-entrypoint.sh
