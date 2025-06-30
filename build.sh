#!/usr/bin/env bash
# Instala dependencias y realiza migraciones automáticamente

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
