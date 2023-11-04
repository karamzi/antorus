#!/bin/bash

python manage.py collectstatic --noinput

python manage.py makemigrations main
python manage.py migrate

# Start server
uwsgi --strict --ini uwsgi.ini
