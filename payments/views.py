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
from .models import Payment


def _mpesa_password() -> str:
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    encoded_string = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')
    return encoded_string, timestamp


def _mpesa_token() -> str:
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
            "AccountReference": f"ORDER{order.id}",
            "TransactionDesc": "Campus Shoppy Order Payment"
        }

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
        metadata = result.get('CallbackMetadata', {}).get('Item', [])
        receipt = next((i['Value'] for i in metadata if i.get('Name') == 'MpesaReceiptNumber'), '')
        amount = next((i['Value'] for i in metadata if i.get('Name') == 'Amount'), None)
        if amount is not None:
            payment.amount = amount
        payment.receipt_number = receipt
        payment.status = 'success'
        payment.order.paid = True
        payment.order.save(update_fields=['paid'])
    else:
        payment.status = 'failed'

    payment.save()
    return JsonResponse({'status': payment.status})

