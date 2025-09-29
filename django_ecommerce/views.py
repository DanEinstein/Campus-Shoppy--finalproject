from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """A simple view for the homepage."""
    # Fetch recent products to display on the homepage
    products = Product.objects.order_by('-id')[:8]
    context = {'products': products}
    return render(request, "home.html", context)