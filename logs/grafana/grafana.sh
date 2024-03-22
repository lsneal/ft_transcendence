#!/bin/sh

sleep 2
export VAULT_TOKEN=$(cat /opt/grafana_token)
export GRAFANA_USERNAME=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://vault:8200/v1/kv/grafana | sed -n 's/.*"data":{"\([^"]*\)":"\([^"]*\).*/\1/p')
export GRAFANA_PASSWORD=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://vault:8200/v1/kv/grafana | sed -n 's/.*"data":{"\([^"]*\)":"\([^"]*\).*/\2/p')

export DATABASE_USERS=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://vault:8200/v1/database/static-creds/devops_users | sed -n 's/.*"password":"\([^"]*\).*/\1/p')
export DATABASE_PONG=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://vault:8200/v1/database/static-creds/devops_pong | sed -n 's/.*"password":"\([^"]*\).*/\1/p')
# ADD LAST DB

exec grafana server --homepath /usr/share/grafana/ --config /etc/grafana.ini