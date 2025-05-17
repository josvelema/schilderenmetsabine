import os
import django

# Zorg dat de juiste settings geladen worden
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schilderen_site.settings.production")

# Django initialiseren
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="josdev",
        email="rjvelemail@gmail.com",
        password="afrit2332"
    )
    print("✅ Superuser created!")
else:
    print("❗Superuser already exists.")
