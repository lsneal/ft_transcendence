FROM python:3.12.1-alpine3.19

RUN apk add --update --no-cache postgresql-client

RUN pip install --upgrade pip && pip install django \
                                            djangorestframework \
                                            gunicorn \
                                            django-cors-headers \
                                            channels \
                                            uvicorn['standard'] \
                                            hvac 

RUN apk add --no-cache build-base && pip install psycopg2-binary && apk del build-base

WORKDIR /script/mysite

COPY ./startup.sh /run/startup.sh
COPY ./django_postgres_vault /usr/local/lib/python3.12/site-packages
COPY ./vault_pong.py /script/vault_pong.py

ENTRYPOINT ["/run/startup.sh"]
