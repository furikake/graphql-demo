FROM gliderlabs/alpine:3.4

RUN apk add --update \
        python3 \
        bash \
        su-exec \
    && pip3 install --upgrade pip \
    && rm /var/cache/apk/*

ENV APP_PATH /restapi

WORKDIR ${APP_PATH}

COPY requirements.txt *.py schema.sql run-in-docker.sh ./

RUN pip3 install -r requirements.txt

# sqlite DB mount point
VOLUME ["${APP_PATH}/db"]

EXPOSE 8000

CMD ["./run-in-docker.sh"]