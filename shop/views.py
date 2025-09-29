from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Wishlist
from django.contrib.auth.decorators import login_required


def home(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False).select_related('category', 'author')
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/home.html', context)


def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter(is_draft=False).select_related('category', 'author')
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product_details(request, product_id):
    product_details = get_object_or_404(Product.objects.select_related('category', 'author'), id=product_id)
    related_products = Product.objects.filter(category=product_details.category).exclude(id=product_id)[:8]
    context = {
        'product': product_details,
        'related_products': related_products
    }
    return render(request, 'shop/product-details.html', context)


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'shop/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

