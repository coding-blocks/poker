#! /usr/bin/env sh

/usr/sbin/crond
python manage.py migrate
nginx
python manage.py collectstatic --noinput
gunicorn poker.wsgi -b 0.0.0.0:8000