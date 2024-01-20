FROM alpine:3.18

#RUN apk add --update --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community prometheus-node-exporter

COPY ./prometheus.yml /etc/prometheus/prometheus.yml
COPY ./prometheus.sh /run/prometheus.sh

ENTRYPOINT ["/run/prometheus.sh"]
