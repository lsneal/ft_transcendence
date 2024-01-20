FROM alpine:3.18

#RUN apk add --update --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community prometheus-node-exporter

COPY ./prometheus.yml /etc/prometheus/prometheus.yml
COPY ./prometheus.sh /run/prometheus.sh

RUN wget https://github.com/prometheus/prometheus/releases/download/v2.49.0-rc.2/prometheus-2.49.0-rc.2.linux-amd64.tar.gz \
	&& tar xvf prometheus-2.49.0-rc.2.linux-amd64.tar.gz

ENTRYPOINT ["/run/prometheus.sh"]
