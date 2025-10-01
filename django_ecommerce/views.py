from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """Homepage view with products."""
    try:
        products = Product.objects.all()[:8]  # Get first 8 products
    except Exception:
        products = []
    
    context = {
        'products': products
    }
    return render(request, "home.html", context)