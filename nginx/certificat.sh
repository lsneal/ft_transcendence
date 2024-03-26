#!/bin/sh

mkdir /etc/nginx/certs
python /opt/pki.py

sleep 1

mkdir /var/log/nginx/

/usr/sbin/nginx -g "daemon off;"