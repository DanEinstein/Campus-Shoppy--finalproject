from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
import requests
from decimal import Decimal
from .models import Payment
from cart.models import Order
from cart.cart import Cart


class PaystackPaymentView(View):
    """Handle Paystack payment initialization"""
    
    @method_decorator(login_required)
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Create or get payment record
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'payment_method': 'paystack',
                'email': request.user.email,
                'amount': order.total_amount,
                'status': 'pending'
            }
        )
        
        if not created:
            payment.amount = order.total_amount
            payment.email = request.user.email
            payment.save()
        
        return render(request, 'payments/paystack_initiate.html', {
            'order': order,
            'payment': payment,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        })


class PaystackInitializeView(View):
    """Initialize Paystack payment"""
    
    @method_decorator(login_required)
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Check if Paystack credentials are configured
        if not settings.PAYSTACK_SECRET_KEY:
            return JsonResponse({
                'status': 'error',
                'message': 'Paystack credentials not configured. Please set PAYSTACK_SECRET_KEY environment variable.'
            })
        
        try:
            # Initialize Paystack payment
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            
            # Convert amount to cents (Paystack uses cents for KES)
            amount_in_cents = int(float(order.total_amount) * 100)
            
            # Generate unique reference with timestamp to avoid duplicates
            import time
            import random
            unique_reference = f'CAMPUS-SHOPPY-{order.id}-{int(time.time())}-{random.randint(1000, 9999)}'
            
            # Ensure user has a valid email
            user_email = request.user.email
            if not user_email or user_email.strip() == '':
                # Generate a temporary email if user doesn't have one
                user_email = f'user{request.user.id}@campus-shoppy.com'
                print(f"DEBUG: User {request.user.username} has no email, using fallback: {user_email}")
            
            payload = {
                'email': user_email,
                'amount': amount_in_cents,
                'currency': 'KES',  # Kenyan Shilling
                'reference': unique_reference,
                'callback_url': settings.PAYSTACK_CALLBACK_URL,
                'metadata': {
                    'order_id': order.id,
                    'user_id': request.user.id,
                    'username': request.user.username,
                    'custom_fields': [
                        {
                            'display_name': 'Order ID',
                            'variable_name': 'order_id',
                            'value': str(order.id)
                        },
                        {
                            'display_name': 'Username',
                            'variable_name': 'username',
                            'value': request.user.username
                        }
                    ]
                }
            }
            
            print(f"DEBUG: Paystack Request - Amount: {amount_in_cents}, Reference: {unique_reference}")
            print(f"DEBUG: User Email: {user_email}, Username: {request.user.username}")
            print(f"DEBUG: Payload Email: {payload['email']}")
            
            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"DEBUG: Paystack API Response Status: {response.status_code}")
            print(f"DEBUG: Paystack API Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    # Update payment record
                    payment = Payment.objects.get(order=order)
                    payment.paystack_reference = data['data']['reference']
                    payment.paystack_access_code = data['data']['access_code']
                    payment.status = 'pending'
                    payment.save()
                    
                    return JsonResponse({
                        'status': 'success',
                        'authorization_url': data['data']['authorization_url'],
                        'access_code': data['data']['access_code'],
                        'reference': data['data']['reference']
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': data.get('message', 'Failed to initialize payment')
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Payment initialization failed. Status: {response.status_code}, Response: {response.text}'
                })
                
        except Exception as e:
            print(f"DEBUG: Payment Error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Payment error: {str(e)}'
            })


@csrf_exempt
@require_http_methods(["POST"])
def paystack_callback(request):
    """Handle Paystack payment callback"""
    try:
        # Verify the webhook signature (optional but recommended)
        body = request.body
        data = json.loads(body)
        
        reference = data.get('data', {}).get('reference')
        if not reference:
            return JsonResponse({'status': 'error', 'message': 'No reference provided'})
        
        # Get payment record
        try:
            payment = Payment.objects.get(paystack_reference=reference)
        except Payment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Payment not found'})
        
        # Verify payment with Paystack
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        verify_response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers,
            timeout=30
        )
        
        if verify_response.status_code == 200:
            verify_data = verify_response.json()
            
            if verify_data.get('status') and verify_data['data']['status'] == 'success':
                # Payment successful
                payment.status = 'success'
                payment.result_code = '00'
                payment.result_desc = 'Payment successful'
                payment.receipt_number = verify_data['data'].get('reference', '')
                payment.order.paid = True
                payment.order.save()
                payment.save()
                
                # Clear the cart
                cart = Cart(request)
                cart.clear()
                
                return JsonResponse({'status': 'success'})
            else:
                # Payment failed
                payment.status = 'failed'
                payment.result_code = verify_data['data'].get('status', 'failed')
                payment.result_desc = verify_data['data'].get('gateway_response', 'Payment failed')
                payment.save()
                
                return JsonResponse({'status': 'failed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Verification failed'})
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def paystack_success(request, order_id):
    """Display payment success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order)
    
    # Clear the cart after successful payment
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'payments/paystack_success.html', {
        'order': order,
        'payment': payment
    })


@login_required
def paystack_status(request, order_id):
    """Check payment status"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order)
    
    # If payment is successful, clear the cart
    if payment.status == 'success':
        cart = Cart(request)
        cart.clear()
    
    return render(request, 'payments/paystack_status.html', {
        'order': order,
        'payment': payment
    })
