from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<int:order_id>/', views.initiate_payment, name='initiate'),
    path('status/<int:order_id>/', views.payment_status, name='status'),
    path('success/<int:order_id>/', views.payment_status, name='success'),
    path('verify/<int:order_id>/', views.verify_payment, name='verify'),
    path('confirm/<int:order_id>/', views.confirm_payment, name='confirm'),
    path('callback/', views.mpesa_callback, name='callback'),
]

