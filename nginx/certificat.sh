#!/bin/sh

python /opt/pki.py

sleep 1

mkdir /var/log/nginx/

exec /usr/sbin/nginx -g "daemon off;"