#!/bin/sh

if [ -f key.txt ]; then

    vault server --config=/vault/config/conf.json &

    sleep 2

    key1=$(cat key.txt | grep "Key 1" | awk '{print $4}')
    key2=$(cat key.txt | grep "Key 2" | awk '{print $4}')
    key3=$(cat key.txt | grep "Key 3" | awk '{print $4}')
    token=$(cat key.txt | grep Token | awk '{print $4}')

    vault operator unseal $key1
    vault operator unseal $key2
    vault operator unseal $key3

    wait $!
else
    
    vault server --config=/vault/config/conf.json &

    sleep 2

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

    vault secrets enable database

    vault secrets enable kv
    private_key_django=$(openssl rand -hex 32)
    vault kv put kv/django_secrets django_key=$private_key_django

    vault kv put kv/elasticsearch username=motdepassword

    vault policy write django_users_certif policies_users.hcl
    vault token create -policy="django_users_certif" | grep -o 'hvs\.[^\ ]*' > users_token
    mv users_token /django_users_token

    vault policy write django_pong_certif policies_pong.hcl
    vault token create -policy="django_pong_certif" | grep -o 'hvs\.[^\ ]*' > pong_token
    mv pong_token /django_pong_token

    vault policy write nginx_certif policies_nginx.hcl
    vault token create -policy="nginx_certif" | grep -o 'hvs\.[^\ ]*' > n_token
    mv n_token /nginx_token

    vault policy write devops_certif policies_devops.hcl
    vault token create -policy="devops_certif" | grep -o 'hvs\.[^\ ]*' > dvps_token 
    mv dvps_token /devops_token

    vault secrets enable pki

    wait $!

fi