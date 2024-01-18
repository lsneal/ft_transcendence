#!/bin/sh
sleep 5

python manage.py makemigrations
python manage.py migrate

#change the port
exec gunicorn --reload --bind 0.0.0.0:8001 mysite.wsgi:application
