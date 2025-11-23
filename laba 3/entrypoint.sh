#!/bin/bash

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

alembic upgrade head

exec "$@"