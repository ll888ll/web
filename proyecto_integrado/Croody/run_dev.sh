#!/bin/bash
cd /home/666/UNIVERSIDAD/repo/proyecto_integrado/Croody
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=croody.settings.development
export DEBUG=true
export ALLOWED_HOSTS='localhost,127.0.0.1,0.0.0.0'
python manage.py runserver 0.0.0.0:8000
