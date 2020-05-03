FROM nginx
LABEL maintainer="j.drotleff@desk-lab.de"

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
RUN ls

RUN mkdir /www
RUN mkdir /www/data

RUN mv dist /www/data
RUN rm -rf ./*

RUN apt-get clean
RUN apt-get remove --purge -y curl gnupg nodejs build-essential

COPY etc/nginx.conf /etc/nginx/conf.d/default.conf

RUN chown -R www-data /www/data

EXPOSE 8000
