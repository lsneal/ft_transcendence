#!/bin/sh

CONTAINER_FIRST_STARTUP="django"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    python /script/vault_dashboard.py  
fi

python manage.py makemigrations dashboard
python manage.py migrate dashboard

exec gunicorn --bind 0.0.0.0:8004 dashboard.wsgi:application

