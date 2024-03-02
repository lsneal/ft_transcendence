#!/bin/sh

docker exec django_pong python manage.py makemigrations
docker exec django_pong python manage.py migrate
