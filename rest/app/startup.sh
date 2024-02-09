#!/bin/sh
sleep 50

token=$(cat /opt/default_token)
export VAULT_TOKEN=$token

python auth.py

python manage.py migrate
#exec python manage.py runserver 0.0.0.0:8002
exec gunicorn --reload --bind 0.0.0.0:8001 mysite.wsgi:application


# su postgres
# psql
# \d 