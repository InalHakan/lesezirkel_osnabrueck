"""
WSGI config for lesezirkel_osnabrueck project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add project directory to Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Determine which settings to use
if os.environ.get('DJANGO_PRODUCTION'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesezirkel_osnabrueck.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesezirkel_osnabrueck.settings')

# Load environment variables from .env file (production)
try:
    from decouple import config
    # Environment variables will be loaded automatically
except ImportError:
    pass

application = get_wsgi_application()
