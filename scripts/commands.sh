#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

wait_psql.sh
collectstatic.sh
migrate.sh

if [ "${DJANGO_ENV:-development}" = "production" ]; then
    python manage.py check --deploy
    run_production.sh
else
    runserver.sh
fi
