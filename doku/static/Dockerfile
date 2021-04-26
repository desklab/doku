FROM node:16 AS build
LABEL maintainer="j.drotleff@desk-lab.de"

WORKDIR /usr/src/doku
COPY package*.json ./
RUN npm ci
RUN npm rebuild node-sass --unsafe-perm

COPY . .
RUN npm run build

FROM httpd:2.4
RUN rm -rf /usr/local/apache2/htdocs/*
RUN mkdir /usr/local/apache2/htdocs/static
COPY --from=build /usr/src/doku/dist/ /usr/local/apache2/htdocs/static/
COPY ./doku-httpd.conf /usr/local/apache2/conf/httpd.conf
