from django.urls import path
from . import views


urlpatterns = [
    path('', views.shop_page, name='shop'),
    path(
        'product/<product_id>', views.product_details, name='product-details'
    ),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<product_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<item_id>', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

