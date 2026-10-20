#!/bin/sh

exec gunicorn project.asgi:application \
    --bind 0.0.0.0:8000 \
    --worker-class uvicorn_worker.UvicornWorker \
    --workers "${GUNICORN_WORKERS:-3}" \
    --access-logfile - \
    --error-logfile - \
    --timeout "${GUNICORN_TIMEOUT:-0}"
