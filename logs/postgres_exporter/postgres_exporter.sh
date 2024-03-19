#!/bin/sh

export USERNAME='devops'
export USER_PASSWORD='-xv2C5iSgr3EacGTXtqi'
export PONG_PASSWORD='ut60t8AGr6LZ7-ognDOx'
export DATA_SOURCE_NAME="postgresql://${USERNAME}:${USER_PASSWORD}@postgres_users:5432/postgres?sslmode=disable,postgresql://${USERNAME}:${PONG_PASSWORD}@postgres_pong:5433/postgres?sslmode=disable"


exec /bin/postgres_exporter