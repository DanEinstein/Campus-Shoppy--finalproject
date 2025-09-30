from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """A simple view for the homepage."""
    # Fetch recent products to display on the homepage
    products = Product.objects.filter(is_draft=False).order_by('-id')[:8]
    featured_products = Product.objects.filter(is_draft=False, featured=True)[:8]
    context = {
        'products': products,
        'featured_products': featured_products
    }
    return render(request, "home_mobile.html", context)