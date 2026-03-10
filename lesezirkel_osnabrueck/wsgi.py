"""
WSGI config for lesezirkel_osnabrueck project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings on the server to avoid DB mismatches
is_production = (
	os.environ.get('PRODUCTION', '').lower() in ('true', '1', 'yes') or
	os.path.exists('/var/www/lesezirkel-os.de')
)

if is_production:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesezirkel_osnabrueck.settings_production')
else:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesezirkel_osnabrueck.settings')

application = get_wsgi_application()
