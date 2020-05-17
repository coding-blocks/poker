#! /usr/bin/env sh

/usr/sbin/crond
python manage.py migrate
yes yes| python manage.py collectstatic
nginx
gunicorn poker.wsgi -b 0.0.0.0:8000
