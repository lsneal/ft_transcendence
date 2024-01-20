#!/bin/sh

docker exec django3 python manage.py makemigrations
docker exec django3 python manage.py migrate
