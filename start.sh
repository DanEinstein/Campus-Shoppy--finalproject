#!/bin/bash
# Startup script for Render deployment

echo "Starting Campus Shoppy..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=django_ecommerce.settings

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --run-syncdb

# Run database fix script
echo "Running database fix script..."
python fix_db.py

# Run final migrations
echo "Running final migrations..."
python manage.py migrate

# Start gunicorn
echo "Starting gunicorn server..."
exec gunicorn -c gunicorn.conf.py
