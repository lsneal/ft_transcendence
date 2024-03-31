#!/bin/sh

CONTAINER_FIRST_STARTUP="django"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    python /script/vault_pong.py  
fi

python manage.py makemigrations
python manage.py migrate

exec python -m gunicorn --bind 0.0.0.0:8003 -w 1 -k uvicorn.workers.UvicornWorker game.asgi:application

