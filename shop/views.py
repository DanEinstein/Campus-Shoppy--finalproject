from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
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
    try:
        category = Category.objects.all()
        products = Product.objects.filter(is_draft=False).select_related('category', 'author')
    except Exception as e:
        # If there's any database error, use empty querysets
        category = Category.objects.none()
        products = Product.objects.none()
    
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product_details(request, product_id):
    try:
        product_details = get_object_or_404(Product.objects.select_related('category', 'author'), id=product_id)
        related_products = Product.objects.filter(category=product_details.category).exclude(id=product_id)[:8]
    except Exception as e:
        # If there's any database error, return 404
        from django.http import Http404
        raise Http404("Product not found")
    
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
    return redirect('shop:wishlist')


@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('shop:wishlist')


def debug_images(request):
    """Debug view to check product images"""
    products = Product.objects.all()[:10]  # Get first 10 products
    debug_data = []
    
    for product in products:
        photo_info = {
            'id': product.id,
            'name': product.name,
            'has_photo': bool(product.photo),
            'photo_url': None,
            'photo_name': None,
            'photo_exists': False,
            'photo_size': 0
        }
        
        if product.photo:
            try:
                photo_info['photo_url'] = product.photo.url
                photo_info['photo_name'] = product.photo.name
                photo_info['photo_exists'] = product.photo.storage.exists(product.photo.name)
                photo_info['photo_size'] = product.photo.size if hasattr(product.photo, 'size') else 0
            except Exception as e:
                photo_info['photo_error'] = str(e)
        
        debug_data.append(photo_info)
    
    return JsonResponse({
        'products': debug_data,
        'total_products': Product.objects.count(),
        'products_with_images': Product.objects.exclude(photo='').count(),
        'products_without_images': Product.objects.filter(photo='').count(),
        'media_url': settings.MEDIA_URL,
        'media_root': str(settings.MEDIA_ROOT)
    })


def test_image_upload(request):
    """Test view to check if image uploads are working"""
    if request.method == 'POST':
        # This would be for testing file uploads
        pass
    
    return render(request, 'shop/test_upload.html', {
        'media_url': settings.MEDIA_URL,
        'media_root': str(settings.MEDIA_ROOT)
    })


def debug_media_files(request):
    """Debug view to check media file serving"""
    import os
    from django.conf import settings
    
    # Check if media directory exists
    media_exists = os.path.exists(settings.MEDIA_ROOT)
    
    # Get list of files in media directory
    media_files = []
    if media_exists:
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), settings.MEDIA_ROOT)
                media_files.append({
                    'name': file,
                    'path': rel_path,
                    'full_path': os.path.join(root, file),
                    'url': f"{settings.MEDIA_URL}{rel_path.replace(os.sep, '/')}"
                })
    
    return JsonResponse({
        'media_url': settings.MEDIA_URL,
        'media_root': str(settings.MEDIA_ROOT),
        'media_exists': media_exists,
        'debug': settings.DEBUG,
        'files': media_files[:10],  # Limit to first 10 files
        'total_files': len(media_files)
    })

