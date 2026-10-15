FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.1 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/venv \
    UV_NO_CACHE=1 \
    PYTHONPATH=/agent_app/src \
    PATH="/venv/bin:$PATH"

WORKDIR /agent_app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project --no-cache

COPY src ./src

CMD ["python", "-m", "celery", "-A", "main:app", "worker", "--loglevel=INFO", "--concurrency=1"]
