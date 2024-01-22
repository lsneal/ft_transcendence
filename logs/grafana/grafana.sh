#!/bin/sh

exec grafana server --homepath /usr/share/grafana/ --config /etc/grafana.ini
