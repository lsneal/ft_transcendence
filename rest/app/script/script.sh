#!/bin/sh

curl -X PUT -H "X-Vault-Request: true" -H "X-Vault-Token: $(vault print token)" -d '{"key":"value"}' http://127.0.0.1:8200/v1/kv/secret_name
