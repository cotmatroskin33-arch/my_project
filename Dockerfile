FROM python:3.12.12-slim AS builder

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install --no-cache-dir poetry==2.4.1

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-interaction --no-ansi


FROM python:3.12.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN useradd --create-home appuser

COPY --from=builder /app/.venv /app/.venv

COPY --chown=appuser:appuser alembic ./alembic
COPY --chown=appuser:appuser alembic.ini .
COPY --chown=appuser:appuser src ./src

USER appuser

CMD ["uvicorn", "src.application:get_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
