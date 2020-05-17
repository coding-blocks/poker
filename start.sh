#! /usr/bin/env sh

/usr/sbin/crond
python manage.py migrate
nginx
echo 'yes' | python manage.py collectstatic
gunicorn poker.wsgi -b 0.0.0.0:8000