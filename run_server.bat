@echo off
echo Starting Campus Shoppy Server...
echo.
echo Make sure you're in the project directory: C:\Users\User\Desktop\Campus Shoppy
echo.
echo Activating virtual environment and starting server...
echo.
call venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
pause
