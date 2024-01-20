#!/bin/sh

node_exporter &

exec prometheus-2.49.0-rc.2.linux-amd64/prometheus --config.file=/etc/prometheus/prometheus.yml
