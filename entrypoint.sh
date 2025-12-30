#!/bin/sh
set -e

echo "⏳ Esperando a la base de datos..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ Base de datos disponible"

echo "📦 Ejecutando migraciones Alembic..."
alembic upgrade head

echo "🚀 Iniciando aplicación..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
