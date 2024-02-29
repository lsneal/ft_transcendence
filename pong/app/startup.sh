#!/bin/sh

python manage.py makemigrations game
python manage.py migrate game

#change the port
#exec python -m gunicorn -k uvicorn.workers.UvicornWorker game.asgi:application & 
#exec python manage.py runserver shell 0.0.0.0:8003
#exec python -m gunicorn --reload  --bind 0.0.0.0:8003 -w 1 -k uvicorn.workers.UvicornWorker game.asgi:application --log-level 'debug' --access-logfile '-' --error-logfile  '-'
exec python -m gunicorn --bind 0.0.0.0:8003 -w 1 -k uvicorn.workers.UvicornWorker game.asgi:application

