#!/bin/sh

export VAULT_TOKEN=$(cat /opt/kibana_token)
export ELASTICSEARCH_USERNAME=kibana_system
jsoncreds=$(curl --request GET --header "X-Vault-Token: $VAULT_TOKEN" http://vault:8200/v1/kv/kibana)
export ELASTICSEARCH_PASSWORD=$($jsoncreds | sed -n 's/.*"kibana_system":"\([^"]*\).*/\1/p')

/usr/local/bin/kibana-docker