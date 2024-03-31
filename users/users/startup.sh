#!/bin/sh

CONTAINER_FIRST_STARTUP="django"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    python /script/vault_users.py  
fi

python manage.py makemigrations users
python manage.py migrate users
exec gunicorn --bind 0.0.0.0:8002 users.wsgi:application
