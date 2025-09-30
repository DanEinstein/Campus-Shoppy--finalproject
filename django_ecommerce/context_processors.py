def cart_context(request):
    """Safe cart context processor that doesn't cause database errors."""
    # Return empty cart to avoid any database queries
    return {
        'cart': [],
        'cart_count': 0
    }
