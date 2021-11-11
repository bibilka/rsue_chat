"""
ASGI config for thebestchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

# from django.core.asgi import get_asgi_application
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thebestchat.settings')

django.setup()
application = get_default_application()
# application = get_asgi_application()
