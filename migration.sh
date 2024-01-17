#!/bin/sh

docker exec django python manage.py makemigrations
docker exec django python manage.py migrate
