#!/bin/sh
sleep 5

python manage.py makemigrations
python manage.py migrate

#change the port
#exec python -m gunicorn -k uvicorn.workers.UvicornWorker mysite.asgi:application & 
#exec python manage.py runserver shell 0.0.0.0:8003
exec python -m gunicorn --reload  --bind 0.0.0.0:8003 -w 1 -k uvicorn.workers.UvicornWorker mysite.asgi:application --log-level 'debug' --access-logfile '-' --error-logfile  '-'
