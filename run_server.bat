@echo off
echo Starting Campus Shoppy Server...
echo.
echo Make sure you're in the project directory: C:\Users\User\Desktop\Campus Shoppy
echo.
echo Activating virtual environment and starting server...
echo.
call venv\Scripts\activate

REM Set Django settings for better connection handling
set DJANGO_SETTINGS_MODULE=django_ecommerce.settings
set PYTHONUNBUFFERED=1

REM Start server with improved settings
venv\Scripts\python manage.py runserver 127.0.0.1:8000
pause
