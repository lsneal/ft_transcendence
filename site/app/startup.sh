#!/bin/sh
sleep 5

python manage.py makemigrations
python manage.py migrate

#change the port
exec gunicorn --reload --bind 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker mysite.asgi:application --log-level 'debug' --access-logfile '-' --error-logfile  '-'