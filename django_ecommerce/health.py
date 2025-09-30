"""
Health check endpoint for Render deployment
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os


@csrf_exempt
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Campus Shoppy is running',
        'database': 'sqlite3',
        'debug': os.environ.get('DJANGO_DEBUG', 'False')
    })
