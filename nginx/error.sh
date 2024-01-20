#!/bin/sh

docker exec nginx cat /var/log/nginx/error.log
