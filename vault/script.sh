#!/bin/sh

vault server --config=/vault/config/conf.json &

sleep 4

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

sleep 3

vault secrets enable database

vault write database/config/postgres \
    plugin_name="postgresql-database-plugin" \
    allowed_roles="my-rolev1" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/postgres" \
    username="postgres" \
    password="password" \
    password_authentication="scram-sha-256"
#change password and username 

vault write database/roles/my-rolev1 \
    db_name="postgres" \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT ALL PRIVILEGES ON DATABASE postgres TO \"{{name}}\"; \
        ALTER ROLE \"{{name}}\" WITH SUPERUSER;" \
    default_ttl="1h" \
    max_ttl="24h"
# changer la durer d'expiration des creds de la db (ttl)

vault secrets enable kv
private_key_django=$(openssl rand -hex 32)
vault kv put kv/django_secrets django_key=$private_key_django

vault policy write certif policies.hcl
vault token create -policy="certif" | grep -o 'hvs\.[^\ ]*' > token
cp token /opt

wait $! 