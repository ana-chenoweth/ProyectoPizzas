#!/bin/bash
# build.sh

pip install -r requirements.txt

# Migraciones
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Recopilar assets
python manage.py collectstatic --noinput

# Opcional: crea un superusuario si no existe (usa variables de entorno)
python - << 'EOF'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if USERNAME and not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL or '', PASSWORD)
    print("Superuser creado:", USERNAME)
EOF
