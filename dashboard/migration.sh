#!/bin/sh

docker exec django_dashboard python manage.py makemigrations dashboard
docker exec django_dashboard python manage.py migrate dashboard
