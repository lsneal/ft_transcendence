#!/bin/sh

#if [ ! -f prometheus/prometheus ] 
#then 
#	wget https://github.com/prometheus/prometheus/releases/download/v2.49.0-rc.2/prometheus-2.49.0-rc.2.linux-amd64.tar.gz 
#	tar xvf prometheus-2.49.0-rc.2.linux-amd64.tar.gz
#	rm prometheus-2.49.0-rc.2.linux-amd64.tar.gz
#fi

export USERNAME='devops'

exec  prometheus-2.49.0-rc.2.linux-amd64/prometheus --config.file=/etc/prometheus/prometheus.yml
