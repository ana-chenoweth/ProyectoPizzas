#!/usr/bin/env bash

# Instala dependencias
pip install -r requirements.txt

# Migraciones desde dentro de la carpeta MyPizzeria
cd MyPizzeria
python manage.py migrate
