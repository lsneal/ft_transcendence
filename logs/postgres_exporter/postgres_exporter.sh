#!/bin/sh

sleep 2

vaulthostname=$(cat /opt/host/hostname)
export VAULT_TOKEN=$(cat /opt/postgres_exporter_token)
export USERNAME='devops'
export USER_PASSWORD=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://$vaulthostname:8200/v1/database/static-creds/devops_users | sed -n 's/.*"password":"\([^"]*\).*/\1/p')
export PONG_PASSWORD=$(wget --header="X-Vault-Token: $VAULT_TOKEN" -qO - http://$vaulthostname:8200/v1/database/static-creds/devops_pong | sed -n 's/.*"password":"\([^"]*\).*/\1/p')

export DATA_SOURCE_NAME="postgresql://${USERNAME}:${USER_PASSWORD}@postgres_users:5432/postgres?sslmode=disable,postgresql://${USERNAME}:${PONG_PASSWORD}@postgres_pong:5433/postgres?sslmode=disable"


exec /bin/postgres_exporter