@echo off
echo Starting Campus Shoppy Server (Stable Version)...
echo.
echo Make sure you're in the project directory: C:\Users\User\Desktop\Campus Shoppy
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run: python -m venv venv
    echo Then install requirements: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

REM Set environment variables for better connection handling
set DJANGO_SETTINGS_MODULE=django_ecommerce.settings
set PYTHONUNBUFFERED=1
set DJANGO_DEBUG=True

echo.
echo Starting Django development server...
echo Server will be available at: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

REM Start server with stable configuration
python manage.py runserver 127.0.0.1:8000 --noreload --insecure --verbosity=1

echo.
echo Server stopped.
pause
