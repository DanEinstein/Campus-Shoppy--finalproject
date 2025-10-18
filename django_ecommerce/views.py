from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product


def home_view(request):
    """Homepage view with products."""
    try:
        products = Product.objects.all()[:8]  # Get first 8 products
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading products: {e}")
        products = []
    
    context = {
        'products': products
    }
    return render(request, "home.html", context)


def simple_home(request):
    """Simple homepage without base template"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Campus Shoppy</title></head>
    <body>
        <h1>Campus Shoppy</h1>
        <p>Simple homepage working</p>
        <a href="/test/">Test endpoint</a>
        <a href="/minimal/">Minimal test</a>
    </body>
    </html>
    """, content_type='text/html')


def minimal_test(request):
    """Minimal test view that bypasses templates"""
    return HttpResponse("Minimal test working", content_type='text/plain')