#!/bin/sh

python manage.py migrate
#exec python manage.py runserver 0.0.0.0:8002
exec gunicorn --reload --bind 0.0.0.0:8002 users.wsgi:application

