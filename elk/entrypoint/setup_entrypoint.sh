#!/bin/sh

sleep 5
export VAULT_TOKEN=$(cat /opt/elasticsearch_token)
elasticjson=$(curl -s --request GET --header "X-Vault-Token: $VAULT_TOKEN" http://vault:8200/v1/kv/elasticsearch)

export ELASTIC_PASSWORD=$(echo $elasticjson | sed -n 's/.*"elastic":"\([^"]*\).*/\1/p')
kibanajson=$(curl -s --request GET --header "X-Vault-Token: $VAULT_TOKEN" http://vault:8200/v1/kv/kibana)
export KIBANA_PASSWORD=$(echo $kibanajson | sed -n 's/.*"kibana_system":"\([^"]*\).*/\1/p')

if [ x$ELASTIC_PASSWORD == x ]; then
  echo "Set the ELASTIC_PASSWORD environment variable in the .env file";
  exit 1;
elif [ x$KIBANA_PASSWORD == x ]; then
  echo "Set the KIBANA_PASSWORD environment variable in the .env file";
  exit 1;
fi;

if [ ! -f config/certs/ca.zip ]; then
  echo "Creating CA";
  bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
  unzip config/certs/ca.zip -d config/certs;
fi;

if [ ! -f config/certs/certs.zip ]; then
  echo "Creating certs";
  echo -ne \
  "instances:\n"\
  "  - name: es01\n"\
  "    dns:\n"\
  "      - es01\n"\
  "      - localhost\n"\
  "    ip:\n"\
  "      - 127.0.0.1\n"\
  > config/certs/instances.yml;
  bin/elasticsearch-certutil cert --silent --pem -out config/certs/certs.zip --in config/certs/instances.yml --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
  unzip config/certs/certs.zip -d config/certs;
fi;

echo "Setting file permissions"
chown -R 1000:1000 config/certs;
find . -type d -exec chmod 750 \{\} \;;
find . -type f -exec chmod 640 \{\} \;;
echo "Waiting for Elasticsearch availability";
until curl -s --cacert config/certs/ca/ca.crt https://es01:9200 | grep -q "missing authentication credentials"; do echo "Waiting for elasticsearch..."; sleep 10; done;
echo "Setting kibana_system password";
until curl -s -X POST --cacert config/certs/ca/ca.crt -u "elastic:$ELASTIC_PASSWORD" -H "Content-Type: application/json" https://es01:9200/_security/user/kibana_system/_password -d "{\"password\":\"$KIBANA_PASSWORD\"}" | grep -q "^{}"; do sleep 10; done;
echo "Setting done!";

until curl -s -I http://kibana:5601 | grep -q 'HTTP/1.1 302 Found'; do echo "Waiting for kibana..." ; sleep 5; done;
echo "Kibana can be accessed";

dataview=$(until curl -s --cacert config/certs/ca/ca.crt -u "elastic:$ELASTIC_PASSWORD" -H "kbn-xsrf: reporting" -H "Content-Type: application/json" -X POST http://kibana:5601/api/data_views/data_view -d '{
  "data_view": {
     "title": "postgres_*",
     "name": "Users Data View"
  }
}'; do sleep 10; done;)
USER_ID=$(echo $dataview | sed -n 's/.*"id":"\([^"]*\).*/\1/p')
dataview=$(until curl -s --cacert config/certs/ca/ca.crt -u "elastic:$ELASTIC_PASSWORD" -H "kbn-xsrf: reporting" -H "Content-Type: application/json" -X POST http://kibana:5601/api/data_views/data_view -d '{
  "data_view": {
     "title": "nginx*",
     "name": "Nginx Data View"
  }
}'; do sleep 10; done;)
NGINX_ID=$(echo $dataview | sed -n 's/.*"id":"\([^"]*\).*/\1/p')
dataview=$(until curl -s --cacert config/certs/ca/ca.crt -u "elastic:$ELASTIC_PASSWORD" -H "kbn-xsrf: reporting" -H "Content-Type: application/json" -X POST http://kibana:5601/api/data_views/data_view -d '{
  "data_view": {
     "title": "modsec*",
     "name": "ModSecurity Data View"
  }
}'; do sleep 10; done;)
MODSEC_ID=$(echo $dataview | sed -n 's/.*"id":"\([^"]*\).*/\1/p')
echo "Data Views Created";

until curl -s --cacert config/certs/ca/ca.crt -u "elastic:$ELASTIC_PASSWORD" -H "kbn-xsrf: reporting" -H "Content-Type: application/json" -X POST http://kibana:5601/api/kibana/dashboards/import?exclude=index-pattern -d "$(sed 's/dataview_id_to_replace/'${USER_ID}'/g' /etc/dashboards/kibana-dashboards.postgres.json)"; do sleep 10; done;
echo "Dashboard Postgres Imported"

until curl -s --cacert config/certs/ca/ca.crt -u "elastic:$ELASTIC_PASSWORD" -H "kbn-xsrf: reporting" -H "Content-Type: application/json" -X POST http://kibana:5601/api/kibana/dashboards/import?exclude=index-pattern -d "$(sed 's/dataview_id_to_replace/'${NGINX_ID}'/g' /etc/dashboards/kibana-dashboards.nginx.json)"; do sleep 10; done;
echo "Dashboard Nginx Imported"

echo "Dashboards Imported Done!";
