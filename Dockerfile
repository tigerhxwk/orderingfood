FROM alpine:latest

RUN --mount=type=cache,target=/var/cache/apt \
    apk add --no-cache python3 py3-pip tini bash tzdata

ENV TKEY=${TKEY}
ENV TZ=Asia/Novosibirsk

WORKDIR /

COPY parser/requirements.txt /parser/requirements.txt
COPY tgbot/src/requirements.txt /tgbot/src/requirements.txt
COPY tgbot/src/gsheets/requirements.txt /tgbot/src/gsheets/requirements.txt
COPY tgbot/src/gsheets/cred.json /tgbot/src/gsheets/cred.json

RUN --mount=type=cache,target=.cache/pip \
    pip install -r /parser/requirements.txt && \
    pip install -r /tgbot/src/requirements.txt && \
    pip install -r /tgbot/src/gsheets/requirements.txt

COPY parser parser
COPY tgbot tgbot
COPY start.sh start.sh
COPY cron cron

RUN /usr/bin/crontab /cron/crontab.txt

CMD ["/cron/cron.sh"]
