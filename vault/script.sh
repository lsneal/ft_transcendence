#!/bin/sh

vault server --config=/vault/config/conf.json &

sleep 3

vault operator init > key.txt

key1=$(cat key.txt | grep "Key 1" | awk '{print $4}')
key2=$(cat key.txt | grep "Key 2" | awk '{print $4}')
key3=$(cat key.txt | grep "Key 3" | awk '{print $4}')
token=$(cat key.txt | grep Token | awk '{print $4}')

vault operator unseal $key1
vault operator unseal $key2
vault operator unseal $key3

echo "$token" > root_token
export VAULT_TOKEN=$token
curl --header "X-Vault-Token: $token" --request POST --data @payload.json http://127.0.0.1:8200/v1/auth/token/create | jq '.' > default
cat default | grep client_token | awk '{print $2}' | cut -d "\"" -f 2 > default_token
cp default_token /opt

sleep 5

curl --header "X-Vault-Token: hvs.SvYWG8o8BfsGaav13MHA5sLJ" --request GET http://vault:8200/v1

vault secrets enable database

# mettre le on role pour la suite
vault write database/config/postgres \
    plugin_name="postgresql-database-plugin" \
    allowed_roles="my-rolev1" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/postgres" \
    username="postgres" \
    password="password" \
    password_authentication="scram-sha-256"
#
# mettre le bon role dans le path que au debut
vault write database/roles/my-rolev1 \
    db_name="postgres" \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"
GRANT ALL PRIVILEGES ON DATABASE thedatabse TO theotheruser;

# export le token root 
# cree new secret engine avec le root 
# cree un token a partir du root (mais avec moins de privilege)
# partager le token (default token) avec docker django (et les autres si besoin)


wait $! 