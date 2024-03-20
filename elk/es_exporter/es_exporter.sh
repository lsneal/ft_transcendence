#!/bin/sh


# export token 
export VAULT_TOKEN=$(cat /opt/es_exporter_token)
elasticjson=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://vault:8200/v1/kv/elasticsearch)
export ELASTIC_PASSWORD=$(echo $elasticjson | sed -n 's/.*"elastic":"\([^"]*\).*/\1/p')
exec elasticsearch_exporter --es.uri=https://elastic:$ELASTIC_PASSWORD@es01:9200 --es.ca=/certs/ca/ca.crt 