FROM ubuntu:22.04

ARG UID=1000
ARG GID=1000

ENV UID=${UID}
ENV GID=${GID}
ENV TZ=${TZ}

ENV DEBIAN_FRONTEND="noninteractive"

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get -y update && apt-get -y upgrade && \
    apt-get -y install apt-utils python3 pip tzdata locales cron

ENV LANG en_US.utf8

RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN groupadd --gid $GID bot \
  && useradd --uid $UID --gid bot --shell /bin/bash --create-home bot

WORKDIR /home/bot/

ENV PATH = ${PATH}:/home/bot/.local/bin

COPY /parser/requirements.txt /home/bot/parser/requirements.txt
COPY tgbot/src/requirements.txt /home/bot/tgbot/src/requirements.txt

USER bot

RUN --mount=type=cache,target=.cache/pip \
    pip install -r ./parser/requirements.txt && \
    pip install -r ./tgbot/src/requirements.txt

USER root

COPY parser /home/bot/parser
COPY tgbot /home/bot/tgbot
COPY start.sh /home/bot/start.sh
COPY parser/cron_parser /etc/cron.d/cron_parser

RUN chown bot:bot -R /home/bot/parser && \
    chown bot:bot -R /home/bot/tgbot && \
    chown bot:bot    /home/bot/start.sh

RUN service cron start

USER bot

CMD ["./start.sh"]
