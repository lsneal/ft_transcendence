#!/bin/sh

exec elasticsearch_exporter --es.uri=https://elastic:2c5abf358fc4420be235217a83efa31217906288f6962d0bac14cdef54bc1a55@es01:9200 --es.ca=/certs/ca/ca.crt 