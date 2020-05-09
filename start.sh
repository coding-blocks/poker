#! /usr/bin/env sh

/usr/sbin/crond
python manage.py migrate
gunicorn poker.wsgi -b 0.0.0.0:8000