from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """A simple view for the homepage."""
    # Fetch recent products to display on the homepage
    products = Product.objects.filter(is_draft=False).order_by('-id')[:8]
    
    # Try to get featured products, fallback to recent products if featured field doesn't exist
    try:
        featured_products = Product.objects.filter(is_draft=False, featured=True)[:8]
    except Exception:
        # If featured field doesn't exist, use recent products
        featured_products = Product.objects.filter(is_draft=False).order_by('-id')[:8]
    
    context = {
        'products': products,
        'featured_products': featured_products
    }
    return render(request, "home_simple.html", context)