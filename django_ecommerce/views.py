from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """A simple view for the homepage."""
    # Minimal context to avoid database issues
    context = {}
    return render(request, "home_minimal.html", context)