FROM gliderlabs/alpine:3.4

RUN apk add --update \
        python3 \
        bash \
        su-exec \
    && pip3 install --upgrade pip \
    && rm /var/cache/apk/*

COPY requirements.txt *.py schema.sql run-in-docker.sh /restapi/

# sqlite DB mount point
VOLUME ["/restapi/db"]

# a bit hacky but the run.sh command defaults to 0.0.0.0:8000
EXPOSE 8000

CMD ["/restapi/run-in-docker.sh"]