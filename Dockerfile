FROM ubuntu:22.04

ARG UID=1000
ARG GID=1000

ENV UID=${UID}
ENV GID=${GID}
ENV TZ=${TZ}

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install apt-utils python3 pip tzdata locales

ENV LANG en_US.utf8

RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN groupadd --gid $GID bot \
  && useradd --uid $UID --gid bot --shell /bin/bash --create-home bot

WORKDIR /home/bot/

ENV PATH = ${PATH}:/home/bot/.local/bin

COPY parser /home/bot/parser
COPY tgbot /home/bot/tgbot

RUN chown bot:bot -R /home/bot/

USER bot

RUN pip install -r ./parser/requirements.txt && \
    pip install -r ./tgbot/src/requirements.txt
