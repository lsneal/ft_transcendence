#!/bin/sh

docker exec django_pong python manage.py makemigrations game
docker exec django_pong python manage.py migrate game
