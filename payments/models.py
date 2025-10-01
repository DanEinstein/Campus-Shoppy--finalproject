from django.db import models
from django.conf import settings
from cart.models import Order


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('paystack', 'Paystack'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='paystack')
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # For M-Pesa
    email = models.EmailField(blank=True, null=True)  # For Paystack
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # M-Pesa fields
    merchant_request_id = models.CharField(max_length=64, blank=True)
    checkout_request_id = models.CharField(max_length=64, blank=True)
    
    # Paystack fields
    paystack_reference = models.CharField(max_length=100, blank=True)
    paystack_access_code = models.CharField(max_length=100, blank=True)
    
    # Common fields
    result_code = models.CharField(max_length=10, blank=True)
    result_desc = models.CharField(max_length=255, blank=True)
    receipt_number = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, success, failed, cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment for Order {self.order_id} - {self.status}'

