FROM python:3.12.1-alpine3.19

RUN apk add --update --no-cache postgresql-client

RUN pip install --upgrade pip && pip install django djangorestframework gunicorn djangorestframework-simplejwt

RUN apk add --no-cache build-base && pip install psycopg2-binary && apk del build-base

WORKDIR /script/mysite

COPY ./script /script/mysite
COPY ./startup.sh /run/startup.sh

#CMD ["python", "manage.py", "runserver", "django:8000"]
ENTRYPOINT ["/run/startup.sh"]
