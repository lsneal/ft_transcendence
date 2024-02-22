#!/bin/sh
sleep 5

python manage.py makemigrations
python manage.py migrate

#change the port
<<<<<<< HEAD
#exec python -m gunicorn -k uvicorn.workers.UvicornWorker mysite.asgi:application & 
#exec python manage.py runserver shell 0.0.0.0:8003
exec python -m gunicorn --bind 0.0.0.0:8001 -w 1 -k uvicorn.workers.UvicornWorker mysite.asgi:application --log-level 'debug' --access-logfile '-' --error-logfile  '-'
=======
exec python -m gunicorn -k uvicorn.workers.UvicornWorker mysite.asgi:application & 
exec python manage.py runserver shell 0.0.0.0:8003
#exec gunicorn --reload --bind 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker mysite.asgi:application --log-level 'debug' --access-logfile '-' --error-logfile  '-'
>>>>>>> 9dff9849e799b2b735d3643318d060fb041a5044
