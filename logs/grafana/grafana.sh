#!/bin/sh

exec grafana server --homepath /usr/share/grafana/ --config /usr/share/grafana/conf/defaults.ini
