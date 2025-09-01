#!/usr/bin/env bash
set -e

# wait for DB to be available (simple loop)
host="${DATABASE_HOST:-db}"
port="${DATABASE_PORT:-5432}"

echo "Waiting for database ${host}:${port}..."
for i in {1..30}; do
  if nc -z "$host" "$port"; then
    echo "Database is up"
    break
  fi
  sleep 1
done

# Apply migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

exec "$@"
