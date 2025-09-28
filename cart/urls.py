from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]