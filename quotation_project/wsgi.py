"""
WSGI config for quotation_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""


""" 
Contexto:

es un archivo de configuración que actúa como puente entre el servidor web y tu 
aplicación Django, siendo crucial para el despliegue en producción.
"""


import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_project.settings')

application = get_wsgi_application()
