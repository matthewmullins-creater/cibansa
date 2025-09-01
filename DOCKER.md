# Docker packaging and run instructions

Overview
- Dockerfile to build the Django app image
- docker-compose.yml to run app + Postgres
- docker-entrypoint.sh runs migrations and collects static files on container start

Quick start
1. Copy the example env: `.env.example` -> `.env` and fill sensible values.
2. Build and run with docker-compose:

```bash
docker compose up --build
```

Notes
- The project uses Postgres in docker-compose. If you prefer sqlite, update `DATABASES` in your settings or set env to use sqlite and mount `db.sqlite3`.
- The entrypoint waits for the DB, runs `manage.py migrate`, and `collectstatic` before starting gunicorn.

Troubleshooting
- If migrations fail, run: `docker compose run --rm web python manage.py migrate`
- To open a shell: `docker compose run --rm web python manage.py shell`
