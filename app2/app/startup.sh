#!/bin/sh
sleep 5

python manage.py migrate
#exec python manage.py runserver 0.0.0.0:8002
exec gunicorn --bind 0.0.0.0:8002 mysite.wsgi:application
