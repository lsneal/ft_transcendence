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

    # secret key django users
    vault kv put kv/django_secrets_users django_key_users=$(openssl rand -hex 32)

    # secret key django pong
    vault kv put kv/django_secrets_pong django_key_pong=$(openssl rand -hex 32)

    # secret key django dashboard
    vault kv put kv/django_secrets_dashboard django_key_dashboard=$(openssl rand -hex 32)

    # password elastic
    vault kv put kv/elasticsearch elastic=$(openssl rand -hex 32)

    # password kibana
    vault kv put kv/kibana kibana_system=$(openssl rand -hex 32)

    # password grafana
    vault kv put kv/grafana $(openssl rand -hex 10)=$(openssl rand -hex 32)

    # users
    vault policy write django_users_certif policies_users.hcl
    vault token create -policy="django_users_certif" | grep -o 'hvs\.[^\ ]*' > users_token
    mv users_token /django_users_token

    # pong
    vault policy write django_pong_certif policies_pong.hcl
    vault token create -policy="django_pong_certif" | grep -o 'hvs\.[^\ ]*' > pong_token
    mv pong_token /django_pong_token

    #dashboard
    vault policy write django_dashboard_certif policies_dashboard.hcl
    vault token create -policy="django_dashboard_certif" | grep -o 'hvs\.[^\ ]*' > dashboard_token
    mv dashboard_token /django_dashboard_token

    # nginx
    vault policy write nginx_certif policies_nginx.hcl
    vault token create -policy="nginx_certif" | grep -o 'hvs\.[^\ ]*' > n_token
    mv n_token /nginx_token

    # elasticsearch
    vault policy write elasticsearch_certif policies_elasticsearch.hcl
    vault token create -policy="elasticsearch_certif" | grep -o 'hvs\.[^\ ]*' > elasticsearch_token 
    mv elasticsearch_token /token_elastic

    # kibana 
    vault policy write kibana_certif policies_kibana.hcl
    vault token create -policy="kibana_certif" | grep -o 'hvs\.[^\ ]*' > kibana_token
    mv kibana_token /token_kibana

    # logstash
    vault policy write logstash_certif policies_logstash.hcl
    vault token create -policy="logstash_certif" | grep -o 'hvs\.[^\ ]*' > logstash_token
    mv logstash_token /token_logstash

    # grafana
    vault policy write grafana_certif policies_grafana.hcl
    vault token create -policy="grafana_certif" | grep -o 'hvs\.[^\ ]*' > grafana_token
    mv grafana_token /token_grafana

    # ESexporter
    vault policy write es_exporter_certif policies_es_exporter.hcl
    vault token create -policy="es_exporter_certif" | grep -o 'hvs\.[^\ ]*' > es_exporter_token
    mv es_exporter_token /token_ESexporter

    # postgresExporter
    vault policy write postgres_exporter_certif policies_postgres_exporter.hcl
    vault token create -policy="postgres_exporter_certif" | grep -o 'hvs\.[^\ ]*' > postgres_exporter_token
    mv postgres_exporter_token /token_postgresExporter

    mkdir host
    cp /etc/hostname /host

    vault secrets enable pki

    wait $!

fi