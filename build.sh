#!/usr/bin/env bash
pip install -r requirements.txt
echo "▶️ Applying migrations..."
echo "▶️ Making migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
echo "▶️ Creating superuser if needed..."
python manage.py shell < create_admin_user.pypytho