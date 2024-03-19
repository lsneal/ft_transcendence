#!/bin/sh

docker exec django_dashboard python manage.py makemigrations
docker exec django_dashboard python manage.py migrate
