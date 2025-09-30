from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """Emergency homepage view - no database dependencies."""
    # Completely safe - no database queries, no context
    return render(request, "home_emergency.html", {})