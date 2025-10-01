from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.shop_page, name='shop'),
    path('product/<int:product_id>/', views.product_details, name='product-details'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('debug/images/', views.debug_images, name='debug_images'),
    path('test/upload/', views.test_image_upload, name='test_upload'),
]

