FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY flight_optimizer ./flight_optimizer
COPY web/backend ./web/backend

RUN uv pip install --system --no-cache ".[backend]"

WORKDIR /app/web/backend
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
