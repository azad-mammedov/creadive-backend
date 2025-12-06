FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

WORKDIR /app

# System deps (incl. gettext for translations)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl gettext \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y postgresql-client --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
COPY . .

# Folders (local)
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8000
CMD ["/bin/bash", "docker/entrypoint.sh"]
