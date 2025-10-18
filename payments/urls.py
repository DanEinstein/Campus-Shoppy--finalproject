# payments/urls.py
from django.urls import path
from . import views, paystack_views

app_name = 'payments'

urlpatterns = [
    # Paystack
    path('initiate/paystack/<int:order_id>/', paystack_views.PaystackPaymentView.as_view(), name='initiate-paystack'),
    path('verify/paystack/', paystack_views.verify_paystack_payment, name='verify-paystack'),
    path('success/paystack/', paystack_views.payment_success, name='payment-success-paystack'),
    path('failed/paystack/', paystack_views.payment_failed, name='payment-failed-paystack'),

    # M-Pesa
    path('initiate/mpesa/<int:order_id>/', views.initiate_payment, name='initiate-mpesa'),
    path('callback/mpesa/', views.mpesa_callback, name='mpesa-callback'),
    path('status/mpesa/<int:order_id>/', views.payment_status, name='payment-status-mpesa'),
    path('verify/mpesa/<int:order_id>/', views.verify_payment, name='verify-mpesa'),
    path('confirm/mpesa/<int:order_id>/', views.confirm_payment, name='confirm-mpesa'),
]
