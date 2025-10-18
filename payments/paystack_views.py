# payments/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
import requests
from .models import Payment
from cart.models import Order
from cart.cart import Cart
import time
import random

class PaystackPaymentView(View):
    """
    Renders the page that will initiate the Paystack payment popup.
    """
    @method_decorator(login_required)
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user, paid=False)
        except Order.DoesNotExist:
            messages.error(request, "Order not found or has already been paid.")
            return redirect('shop:shop')

        # Generate a unique reference for the payment
        unique_reference = f'CAMPUS-SHOPPY-{order.id}-{int(time.time())}-{random.randint(1000, 9999)}'

        # Create or update the payment record with the reference
        payment, _ = Payment.objects.update_or_create(
            order=order,
            defaults={
                'payment_method': 'paystack',
                'email': request.user.email,
                'amount': order.get_total_cost(),
                'reference': unique_reference,
                'status': 'pending'
            }
        )

        context = {
            'order': order,
            'payment': payment,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        }
        return render(request, 'payments/paystack_initiate.html', context)

@login_required
def verify_paystack_payment(request):
    """
    Handles the redirect from Paystack after a payment attempt.
    This is the most important view for security.
    """
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, "Payment verification failed: No reference ID provided.")
        return redirect('payments:payment-failed')

    # Prepare to verify the transaction with Paystack's API
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()

        if response_data.get('status') and response_data.get('data') and response_data['data'].get('status') == 'success':
            amount_paid_kobo = response_data['data'].get('amount')
            if amount_paid_kobo is None:
                messages.error(request, "Payment verification failed: Amount not found in response.")
                return redirect('payments:payment-failed')

            payment = get_object_or_404(Payment, reference=reference)
            order = payment.order
            
<<<<<<< HEAD
            if verify_data.get('status') and verify_data['data']['status'] == 'success':
                # CRITICAL: Verify amount matches to prevent fraud
                paid_amount = Decimal(str(verify_data['data']['amount'])) / 100  # Convert from cents
                expected_amount = payment.order.total_amount
                
                # Allow 1 cent difference for rounding
                if abs(paid_amount - expected_amount) > Decimal('0.01'):
                    # Amount mismatch - potential fraud!
                    payment.status = 'failed'
                    payment.result_desc = f'Amount mismatch: Paid {paid_amount}, Expected {expected_amount}'
                    payment.save()
                    
                    # Log this for security review
                    import logging
                    logger = logging.getLogger('payments')
                    logger.error(f'PAYMENT FRAUD ATTEMPT: Order {payment.order.id}, Reference {payment.paystack_reference}, Paid {paid_amount}, Expected {expected_amount}')
                    
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Payment amount verification failed'
                    }, status=400)
                
                # Payment successful and amount verified
=======
            # CRITICAL: Verify the amount paid matches the order total
            if int(amount_paid_kobo) >= int(order.get_total_cost() * 100):
                order.paid = True
                order.save()
>>>>>>> e98667db69d90c224f57b1968017e6c7d554d3cd
                payment.status = 'success'
                payment.save()
<<<<<<< HEAD
                
                # Decrement inventory for each item in the order
                for item in payment.order.items.all():
                    product = item.product
                    product.inventory -= item.quantity
                    product.save(update_fields=['inventory'])
                
                # Clear the cart (Note: This is in webhook, so no user session available)
                # Cart clearing happens in the success view instead
                
                return JsonResponse({'status': 'success'})
=======

                Cart(request).clear()
                messages.success(request, "Your payment was successful!")
                return redirect('payments:payment-success')
>>>>>>> e98667db69d90c224f57b1968017e6c7d554d3cd
            else:
                # Security check failed: Amount mismatch
                payment.status = 'failed'
                payment.save()
                messages.error(request, f"Payment verification failed: Amount mismatch. We received {amount_paid_kobo/100} but expected {order.get_total_cost()}.")
                return redirect('payments:payment-failed')
        else:
            payment = get_object_or_404(Payment, reference=reference)
            payment.status = 'failed'
            payment.save()
            gateway_message = response_data.get('data', {}).get('gateway_response', 'No details provided.')
            messages.error(request, f"Your payment was not successful. Reason: {gateway_message}")
            return redirect('payments:payment-failed')
            
    except requests.exceptions.RequestException as e:
        messages.error(request, f"A network error occurred: {e}. Please contact support.")
        return redirect('payments:payment-failed')
    except (KeyError, TypeError) as e:
        messages.error(request, f"There was an issue processing the payment response: {e}. Please contact support.")
        return redirect('payments:payment-failed')

# Simple views to show the final status
@login_required
def payment_success(request):
    return render(request, 'payments/payment_success.html')

@login_required
<<<<<<< HEAD
def paystack_success(request, order_id):
    """Display payment success page - with verification"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order)
    
    # SECURITY: Verify payment was actually successful before showing success page
    if payment.status != 'success':
        # Payment not successful - verify with Paystack
        if payment.paystack_reference:
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            
            try:
                verify_response = requests.get(
                    f'https://api.paystack.co/transaction/verify/{payment.paystack_reference}',
                    headers=headers,
                    timeout=30
                )
                
                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    
                    if verify_data.get('status') and verify_data['data']['status'] == 'success':
                        # Verify amount matches
                        paid_amount = Decimal(str(verify_data['data']['amount'])) / 100
                        expected_amount = order.total_amount
                        
                        if abs(paid_amount - expected_amount) <= Decimal('0.01'):
                            # Update payment status
                            payment.status = 'success'
                            payment.result_code = '00'
                            payment.result_desc = 'Payment successful'
                            payment.order.paid = True
                            payment.order.save()
                            payment.save()
                            
                            # Decrement inventory
                            for item in order.items.all():
                                product = item.product
                                product.inventory -= item.quantity
                                product.save(update_fields=['inventory'])
                        else:
                            # Amount mismatch
                            messages.error(request, 'Payment verification failed: Amount mismatch')
                            return redirect('cart:cart_detail')
                    else:
                        messages.error(request, 'Payment was not successful. Please try again.')
                        return redirect('cart:cart_detail')
                else:
                    messages.error(request, 'Unable to verify payment. Please contact support.')
                    return redirect('cart:cart_detail')
            except Exception as e:
                import logging
                logger = logging.getLogger('payments')
                logger.error(f'Payment verification error in success view: {str(e)}')
                messages.error(request, f'Payment verification error. Please contact support.')
                return redirect('cart:cart_detail')
        else:
            messages.error(request, 'No payment reference found')
            return redirect('cart:cart_detail')
    
    # Payment is verified as successful - clear cart and show success
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
=======
def payment_failed(request):
    return render(request, 'payments/payment_failed.html')
>>>>>>> e98667db69d90c224f57b1968017e6c7d554d3cd
