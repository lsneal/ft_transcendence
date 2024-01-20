FROM alpine:3.18

RUN apk add --update --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community grafana

COPY ./grafana.sh /run/grafana.sh

ENTRYPOINT ["/run/grafana.sh"]
