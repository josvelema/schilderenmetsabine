#!/usr/bin/env bash

pip install -r requirements.txt

echo "▶️ Collecting static files..."
python manage.py collectstatic --noinput

echo "▶️ Making migrations..."
python manage.py makemigrations --noinput

echo "▶️ Applying migrations..."
python manage.py migrate --noinput

echo "▶️ Creating superuser if needed..."
python manage.py shell < create_admin_user.py