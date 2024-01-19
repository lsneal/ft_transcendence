#!/bin/sh

docker exec django2 python manage.py makemigrations
docker exec django2 python manage.py migrate
