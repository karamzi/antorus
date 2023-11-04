#!/bin/bash

python manage.py collectstatic --noinput

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

python manage.py makemigrations main
python manage.py migrate

# Start server
uwsgi --strict --ini uwsgi.ini
