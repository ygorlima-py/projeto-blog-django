#!/bin/sh
makemigrations.sh
echo 'Execultando migrate.sh'
python manage.py migrate --noinput
