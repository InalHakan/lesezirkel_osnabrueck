#!/bin/bash

# Deployment script for KulturBrucke project

echo "Starting deployment..."

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --settings=kulturbrucke.settings_production

# Run migrations
python manage.py migrate --settings=kulturbrucke.settings_production

# Create superuser if it doesn't exist (optional)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell --settings=kulturbrucke.settings_production

# Compile translation files
python manage.py compilemessages --settings=kulturbrucke.settings_production

# Restart Gunicorn (if running as service)
sudo systemctl restart gunicorn-kulturbrucke

echo "Deployment completed!"