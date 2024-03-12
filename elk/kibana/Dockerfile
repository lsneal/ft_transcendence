FROM docker.elastic.co/kibana/kibana:8.12.2

COPY ./kibana-entrypoint.sh /usr/local/bin/kibana-entrypoint.sh

ENTRYPOINT ["/bin/tini", "--", "/usr/local/bin/kibana-entrypoint.sh"]

USER 1000