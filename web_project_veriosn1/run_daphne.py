# Файл: run_daphne.py

import os
from django.conf import settings
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_project_veriosn1.settings")
settings.configure()

# Получение ASGI-приложения
application = get_default_application()

