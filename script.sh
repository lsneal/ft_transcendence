#!/bin/sh

export VAULT_TOKEN=$(docker exec -it vault cat root_token)

ELASTIC_PASSWORD=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/kv/elasticsearch)
DATABASE_USERS=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/database/static-creds/postgres_users)
DATABASE_PONG=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/database/static-creds/postgres_pong)
DB_USER_DEVOPS_PONG=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/database/static-creds/devops_pong)
DB_USER_DEVOPS_USERS=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/database/static-creds/devops_users)
KIBANA_PASSWORD=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/kv/kibana)
GRAFANA_PASSWORD=$(curl -s -k --request GET --header "X-Vault-Token: $VAULT_TOKEN" https://vault.localhost/v1/kv/grafana)

echo "Root token Vault: $VAULT_TOKEN"
echo ""

echo "Grafana:"
echo $GRAFANA_PASSWORD | jq '.data'
echo ""

echo "Elastic:"
echo $ELASTIC_PASSWORD | jq '.data'
echo "" 

echo "Kibana:"
echo $KIBANA_PASSWORD | jq '.data'
echo ""

echo "DB_users:"
echo $DATABASE_USERS | jq '.data'
echo ""

echo "DB_pong:"
echo $DATABASE_PONG | jq '.data'
echo ""

echo "DB_users_devops:"
echo $DB_USER_DEVOPS_USERS | jq '.data'
echo ""

echo "DB_pong_devops:"
echo $DB_USER_DEVOPS_PONG | jq '.data'
echo ""