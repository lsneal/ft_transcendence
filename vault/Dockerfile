FROM vault:1.13.3

RUN apk add --no-cache curl \
                        jq \
                        openssl
                        
COPY ./conf/conf.json /vault/config/

COPY ./script.sh .
RUN chmod u+s script.sh
RUN chmod +x script.sh

COPY ./policies/policies_es_exporter.hcl .
COPY ./policies/policies_postgres_exporter.hcl .
COPY ./policies/policies_dashboard.hcl .
COPY ./policies/policies_grafana.hcl .
COPY ./policies/policies_elasticsearch.hcl .
COPY ./policies/policies_kibana.hcl .
COPY ./policies/policies_logstash.hcl .
COPY ./policies/policies_users.hcl .
COPY ./policies/policies_pong.hcl .
COPY ./policies/policies_nginx.hcl .

CMD ["./script.sh"]