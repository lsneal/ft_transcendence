#!/bin/sh

ls
if [ -f key.txt ]; then

    vault server --config=/vault/config/conf.json &

    key1=$(cat key.txt | grep "Key 1" | awk '{print $4}')
    key2=$(cat key.txt | grep "Key 2" | awk '{print $4}')
    key3=$(cat key.txt | grep "Key 3" | awk '{print $4}')
    token=$(cat key.txt | grep Token | awk '{print $4}')

    vault operator unseal $key1
    vault operator unseal $key2
    vault operator unseal $key3

    echo "$token" > root_token
    export VAULT_TOKEN=$token

    private_key_django=$(openssl rand -hex 32)
    vault kv put kv/django_secrets django_key=$private_key_django

    vault policy write certif policies.hcl
    vault token create -policy="certif" | grep -o 'hvs\.[^\ ]*' > token
    cp token /opt
    wait $!
else
    
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
        allowed_roles="*" \
        connection_url="postgresql://{{username}}:{{password}}@postgres_users:5432/postgres" \
        username="postgres" \
        password="password" \
        password_authentication="scram-sha-256"

    vault write -force database/rotate-root/postgres


tee rotation.sql <<EOF
ALTER USER "{{name}}" WITH PASSWORD '{{password}}';
EOF


    vault write database/static-roles/my-rolev1 \
        db_name="postgres" \
        rotation_statements=@rotation.sql \
        username="django" \
        rotation_period=3600

    vault read database/static-roles/my-rolev1

    vault secrets enable kv
    private_key_django=$(openssl rand -hex 32)
    vault kv put kv/django_secrets django_key=$private_key_django

    vault policy write certif policies.hcl
    vault token create -policy="certif" | grep -o 'hvs\.[^\ ]*' > token
    cp token /opt

    wait $!

fi