import base64
import datetime
import json
import requests

from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from cart.models import Order
from cart.cart import Cart
from .models import Payment


def _mpesa_password() -> str:
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    encoded_string = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')
    return encoded_string, timestamp


def _mpesa_token() -> str:
    # Check if M-Pesa credentials are configured
    if not settings.MPESA_CONSUMER_KEY or not settings.MPESA_CONSUMER_SECRET:
        raise ValueError("M-Pesa credentials not configured. Please set MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET in your environment variables.")
    
    url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET), timeout=30)
    response.raise_for_status()
    return response.json()['access_token']


@login_required
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Expect phone in POST or from user profile in a real app
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone:
            return HttpResponseBadRequest('Phone number required')
        
        # Format phone number for M-Pesa (remove spaces, ensure it starts with 254)
        phone = phone.strip().replace(' ', '').replace('-', '')
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+254'):
            phone = phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone
        
        # Validate phone number format
        if len(phone) != 12 or not phone.startswith('254'):
            return render(request, 'payments/failed.html', {
                'order': order, 
                'error': 'Invalid phone number. Use format: 07XXXXXXXX or 254XXXXXXXXX'
            })

        payment, _ = Payment.objects.get_or_create(order=order, defaults={
            'phone_number': phone,
            'amount': order.total_amount,
        })

        password, timestamp = _mpesa_password()
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(order.total_amount),
            "PartyA": phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": f"CAMPUS-SHOPPY-{order.id}",
            "TransactionDesc": "Campus Shoppy - Order Payment"
        }

        try:
            token = _mpesa_token()
            stk_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            resp = requests.post(stk_url, headers=headers, json=payload, timeout=30)
            data = resp.json()
            if resp.status_code == 200 and data.get('ResponseCode') == '0':
                payment.merchant_request_id = data.get('MerchantRequestID', '')
                payment.checkout_request_id = data.get('CheckoutRequestID', '')
                payment.status = 'pending'
                payment.save(update_fields=['merchant_request_id', 'checkout_request_id', 'status'])
                return render(request, 'payments/prompted.html', { 'order': order, 'phone': phone })
            else:
                payment.status = 'failed'
                payment.result_desc = data.get('errorMessage', 'Failed to initiate payment')
                payment.save(update_fields=['status', 'result_desc'])
                return render(request, 'payments/failed.html', { 'order': order, 'error': payment.result_desc })
        except ValueError as e:
            # M-Pesa credentials not configured - show development mode
            payment.status = 'development_mode'
            payment.result_desc = str(e)
            payment.save(update_fields=['status', 'result_desc'])
            return render(request, 'payments/development_mode.html', { 
                'order': order, 
                'phone': phone,
                'error': str(e)
            })
        except Exception as e:
            payment.status = 'failed'
            payment.result_desc = f'M-Pesa API error: {str(e)}'
            payment.save(update_fields=['status', 'result_desc'])
            return render(request, 'payments/failed.html', { 'order': order, 'error': payment.result_desc })

    return render(request, 'payments/initiate.html', { 'order': order })


@csrf_exempt
def mpesa_callback(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid payload')

    result = body.get('Body', {}).get('stkCallback', {})
    checkout_request_id = result.get('CheckoutRequestID')
    result_code = str(result.get('ResultCode'))
    result_desc = result.get('ResultDesc', '')

    try:
        payment = Payment.objects.get(checkout_request_id=checkout_request_id)
    except Payment.DoesNotExist:
        return JsonResponse({'status': 'ignored'})

    payment.result_code = result_code
    payment.result_desc = result_desc

    if result_code == '0':
        # Payment successful
        metadata = result.get('CallbackMetadata', {}).get('Item', [])
        receipt = next((i['Value'] for i in metadata if i.get('Name') == 'MpesaReceiptNumber'), '')
        amount = next((i['Value'] for i in metadata if i.get('Name') == 'Amount'), None)
        if amount is not None:
            payment.amount = amount
        payment.receipt_number = receipt
        payment.status = 'success'
        payment.order.paid = True
        payment.order.save(update_fields=['paid'])
        
        # Note: Cart clearing is handled in the frontend after successful payment
    elif result_code == '1':
        # User cancelled the payment
        payment.status = 'cancelled'
    else:
        # Payment failed for other reasons
        payment.status = 'failed'

    payment.save()
    return JsonResponse({'status': payment.status})


@login_required
def payment_status(request, order_id):
    """View to check payment status for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    try:
        payment = Payment.objects.get(order=order)
        
        # Redirect to success page if payment is successful
        if payment.status == 'success':
            return render(request, 'payments/success.html', {
                'order': order,
                'payment': payment
            })
        
        return render(request, 'payments/status.html', {
            'order': order,
            'payment': payment
        })
    except Payment.DoesNotExist:
        return render(request, 'payments/status.html', {
            'order': order,
            'payment': None
        })


@login_required
def verify_payment(request, order_id):
    """Manually verify payment status with M-Pesa"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        payment = Payment.objects.get(order=order)
        
        # First, check if payment already has a result
        if payment.result_code and payment.result_code != '0':
            return JsonResponse({
                'status': 'success',
                'payment_status': payment.status,
                'result_code': payment.result_code,
                'result_desc': payment.result_desc,
                'message': 'Payment status already determined'
            })
        
        if payment.checkout_request_id:
            # Try M-Pesa query API first
            try:
                token = _mpesa_token()
                print(f"M-Pesa Token: {token[:20]}...")  # Debug: show first 20 chars
                
                query_url = f"{settings.MPESA_BASE_URL}/mpesa/stkpushquery/v1/query"
                password, timestamp = _mpesa_password()
                
                payload = {
                    "BusinessShortCode": settings.MPESA_SHORTCODE,
                    "Password": password,
                    "Timestamp": timestamp,
                    "CheckoutRequestID": payment.checkout_request_id
                }
                
                print(f"Query URL: {query_url}")
                print(f"Payload: {payload}")
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                response = requests.post(query_url, headers=headers, json=payload, timeout=30)
                
                # Debug logging
                print(f"M-Pesa Query Response Status: {response.status_code}")
                print(f"M-Pesa Query Response: {response.text}")
                
                if response.status_code == 200:
                    data = response.json()
                    result_code = data.get('ResultCode')
                    result_desc = data.get('ResultDesc', '')
                    
                    # Update payment status based on query result
                    if result_code == 0:
                        # Payment successful
                        payment.status = 'success'
                        payment.result_code = str(result_code)
                        payment.result_desc = result_desc
                        payment.order.paid = True
                        payment.order.save(update_fields=['paid'])
                        
                        # Clear the cart when payment is successful
                        cart = Cart(request)
                        cart.clear()
                    elif result_code == 1032:
                        # Request cancelled by user
                        payment.status = 'cancelled'
                        payment.result_code = str(result_code)
                        payment.result_desc = result_desc
                    elif result_code == 2001:
                        # Initiator information invalid - this might be a timing issue
                        # Keep status as pending and let user try again
                        payment.status = 'pending'
                        payment.result_code = str(result_code)
                        payment.result_desc = result_desc
                    else:
                        # Other failure codes
                        payment.status = 'failed'
                        payment.result_code = str(result_code)
                        payment.result_desc = result_desc
                    
                    payment.save()
                    
                    return JsonResponse({
                        'status': 'success',
                        'payment_status': payment.status,
                        'result_code': result_code,
                        'result_desc': result_desc
                    })
                else:
                    # If M-Pesa query fails, provide manual verification option
                    return JsonResponse({
                        'status': 'manual_verification',
                        'message': 'M-Pesa query failed. Please check your phone for payment confirmation or try again later.',
                        'payment_status': payment.status,
                        'checkout_request_id': payment.checkout_request_id
                    })
                    
            except Exception as e:
                print(f"M-Pesa query error: {str(e)}")
                # Fallback to manual verification
                return JsonResponse({
                    'status': 'manual_verification',
                    'message': f'M-Pesa API unavailable: {str(e)}. Please check your phone for payment confirmation.',
                    'payment_status': payment.status,
                    'checkout_request_id': payment.checkout_request_id
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'No checkout request ID found'
            })
            
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Payment record not found'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


@login_required
def confirm_payment(request, order_id):
    """Manually confirm payment when M-Pesa query is not available"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(order=order)
            confirmation_type = request.POST.get('confirmation_type')
            
            if confirmation_type == 'success':
                payment.status = 'success'
                payment.result_code = '0'
                payment.result_desc = 'Payment confirmed manually'
                payment.order.paid = True
                payment.order.save(update_fields=['paid'])
                payment.save()
                
                # Clear the cart when payment is confirmed as successful
                cart = Cart(request)
                cart.clear()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment confirmed successfully'
                })
            elif confirmation_type == 'failed':
                payment.status = 'failed'
                payment.result_code = '1'
                payment.result_desc = 'Payment failed - confirmed manually'
                payment.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment marked as failed'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid confirmation type'
                })
                
        except Payment.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Payment record not found'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    # GET request - show confirmation form
    try:
        payment = Payment.objects.get(order=order)
        return render(request, 'payments/confirm.html', {
            'order': order,
            'payment': payment
        })
    except Payment.DoesNotExist:
        return render(request, 'payments/confirm.html', {
            'order': order,
            'payment': None
        })

