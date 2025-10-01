from django.urls import path
from . import views
from .paystack_views import PaystackPaymentView, PaystackInitializeView, paystack_callback, paystack_success, paystack_status

app_name = 'payments'

urlpatterns = [
    # M-Pesa URLs (kept for fallback)
    path('initiate/<int:order_id>/', views.initiate_payment, name='initiate'),
    path('status/<int:order_id>/', views.payment_status, name='status'),
    path('success/<int:order_id>/', views.payment_status, name='success'),
    path('verify/<int:order_id>/', views.verify_payment, name='verify'),
    path('confirm/<int:order_id>/', views.confirm_payment, name='confirm'),
    path('callback/', views.mpesa_callback, name='callback'),
    
    # Paystack URLs
    path('paystack/<int:order_id>/', PaystackPaymentView.as_view(), name='paystack_initiate'),
    path('paystack/initialize/<int:order_id>/', PaystackInitializeView.as_view(), name='paystack_initialize'),
    path('paystack/callback/', paystack_callback, name='paystack_callback'),
    path('paystack/success/<int:order_id>/', paystack_success, name='paystack_success'),
    path('paystack/status/<int:order_id>/', paystack_status, name='paystack_status'),
]

