#!/bin/bash
echo "Starting Campus Shoppy Server..."
echo ""
echo "Make sure you're in the project directory"
echo ""
echo "Activating virtual environment and starting server..."
echo ""
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
