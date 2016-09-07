FROM mhart/alpine-node:6

RUN apk add --update \
        bash \
        su-exec \
    && rm /var/cache/apk/*

COPY *.json *.js .babelrc run-in-docker.sh /app/
COPY src/ /app/src/

EXPOSE 5000

CMD ["/app/run-in-docker.sh"]
