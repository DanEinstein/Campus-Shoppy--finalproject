from django.shortcuts import render
from shop.models import Product


def home_view(request):
    """Beautiful homepage view - no database queries for safety."""
    # No database queries to avoid any schema issues
    context = {}
    return render(request, "home_beautiful.html", context)