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

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip --no-cache-dir install -r requirements.txt
RUN pip install uwsgi

RUN rm -rf ~/.cache/pip/*

COPY . /app/

RUN useradd -m doku
RUN mkdir -p /app/resources
RUN mkdir -p /app/shared
RUN mv /app/docker/* /app/
RUN chmod +x /app/docker-entrypoint.sh
RUN chmod +x /app/healthcheck.sh
RUN chmod +x /app/worker.sh
RUN chown -R doku /app

USER doku

RUN mkdir -p /home/doku/.local/share/fonts

ADD --chown=doku https://raw.githubusercontent.com/googlefonts/nunito/master/fonts/TTF/Nunito-Regular.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/nunito/master/fonts/TTF/Nunito-Bold.ttf /home/doku/.local/share/fonts

ADD --chown=doku https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Bold.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Italic.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Regular.ttf /home/doku/.local/share/fonts

ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-Bold.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-Medium.ttf  /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-Regular.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-Light.ttf  /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-Thin.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-BoldItalic.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-MediumItalic.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-Italic.ttf /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-LightItalic.ttf  /home/doku/.local/share/fonts
ADD --chown=doku https://raw.githubusercontent.com/googlefonts/RobotoMono/master/fonts/ttf/RobotoMono-ThinItalic.ttf /home/doku/.local/share/fonts

EXPOSE 8000
WORKDIR /app

HEALTHCHECK CMD ./healthcheck.sh

CMD ./docker-entrypoint.sh
