"""
WSGI config for VLCwebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

path = 'C:/GitHub/DjangoProjects/VLCwebsite'
if path not in sys.path:
    sys.path.append(path)



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VLCwebsite.settings_production")

from django.contrib.auth.handlers.modwsgi import check_password

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
