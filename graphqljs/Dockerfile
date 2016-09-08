FROM mhart/alpine-node:6

RUN apk add --update \
        bash \
        su-exec \
    && rm /var/cache/apk/*

ENV APP_DIR /app

WORKDIR ${APP_DIR}

COPY *.json *.js run-in-docker.sh ./
COPY src/ ./src/

RUN npm install

EXPOSE 5000

CMD ["./run-in-docker.sh"]
