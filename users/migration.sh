#!/bin/sh

docker exec django_users python manage.py makemigrations
docker exec django_users python manage.py migrate
