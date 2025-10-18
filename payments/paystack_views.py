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
            
            # CRITICAL: Verify the amount paid matches the order total
            if int(amount_paid_kobo) >= int(order.get_total_cost() * 100):
                order.paid = True
                order.save()
                payment.status = 'success'
                payment.save()

                Cart(request).clear()
                messages.success(request, "Your payment was successful!")
                return redirect('payments:payment-success')
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
def payment_failed(request):
    return render(request, 'payments/payment_failed.html')