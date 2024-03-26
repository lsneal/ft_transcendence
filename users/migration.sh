#!/bin/sh

docker exec django_users python manage.py makemigrations users
docker exec django_users python manage.py migrate users
