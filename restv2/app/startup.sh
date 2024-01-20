#!/bin/sh
sleep 5

python manage.py migrate
#exec python manage.py createsuperuser --username admin --email admin@example.com 

exec gunicorn --reload --bind 0.0.0.0:8003 mysite.wsgi:application

