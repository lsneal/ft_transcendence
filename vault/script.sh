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

sleep 5

vault secrets enable database

vault write database/config/postgres \
    plugin_name="postgresql-database-plugin" \
    allowed_roles="my-rolev1" \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/postgres" \
    username="postgres" \
    password="password" \
    password_authentication="scram-sha-256"

vault write database/roles/my-rolev1 \
    db_name="postgres" \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT ALL PRIVILEGES ON DATABASE postgres TO \"{{name}}\"; \
        ALTER ROLE \"{{name}}\" WITH SUPERUSER;" \
    default_ttl="1h" \
    max_ttl="24h"

vault policy write certif policies.hcl

vault token create -policy="certif" | grep -o 'hvs\.[^\ ]*' > token
cp token /opt

# for key django
vault secrets enable kv

private_key_django=$(cat /dev/urandom | head -n 128)
curl -X PUT -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" -d '{"key_django":"clejango"}' http://127.0.0.1:8200/v1/kv/django_secrets
vault kv put kv/django_secrets key=$KEY

wait $! 