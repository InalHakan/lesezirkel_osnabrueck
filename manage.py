#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Automatically detect production environment
    # Production if: Linux server OR PRODUCTION env var is set
    is_production = (
        os.environ.get('PRODUCTION', '').lower() in ('true', '1', 'yes') or
        os.path.exists('/var/www/lesezirkel-os.de')  # Production server path
    )
    
    if is_production:
        settings_module = 'lesezirkel_osnabrueck.settings_production'
    else:
        settings_module = 'lesezirkel_osnabrueck.settings'
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
