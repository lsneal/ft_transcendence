#!/bin/sh

export VAULT_TOKEN=$(cat /opt/kibana_token)
jsoncreds=$(curl -s --request GET --header "X-Vault-Token: $VAULT_TOKEN" http://vault:8200/v1/kv/kibana)
export ELASTICSEARCH_PASSWORD=$(echo $jsoncreds | sed -n 's/.*"kibana_system":"\([^"]*\).*/\1/p')

/usr/local/bin/kibana-docker
