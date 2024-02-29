#!/bin/sh

python /opt/pki.py

sleep 1

/usr/sbin/nginx -g "daemon off;"