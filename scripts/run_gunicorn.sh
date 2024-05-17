#!/bin/sh

set -e

python manage.py migrate
gunicorn --log-file /logs/gunicorn.log --config gunicorn.conf.py taskmaster.wsgi:application
