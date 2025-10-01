# Payment Integration Setup Guide

## Current Payment Methods

### 1. Paystack (Primary - Live)
The application is now configured with **Paystack** as the primary payment method using your live credentials.

### 2. M-Pesa (Fallback)
M-Pesa integration is available as a fallback option for development/testing.

## Paystack Configuration (Live)

### ✅ Live Credentials Configuration
Your Paystack live credentials need to be configured via environment variables:

- **Secret Key**: Set `PAYSTACK_SECRET_KEY` environment variable
- **Public Key**: Set `PAYSTACK_PUBLIC_KEY` environment variable  
- **Callback URL**: `https://campus-shoppy-maseno.onrender.com/payments/paystack/callback/`

### Payment Flow
1. **Customer adds items to cart**
2. **Proceeds to checkout** → Redirects to Paystack payment page
3. **Completes payment** → Paystack processes the payment
4. **Payment success** → Cart is cleared, order is marked as paid
5. **Customer receives confirmation** → Success page with order details

### Features
- ✅ **Live Payments**: Real money transactions
- ✅ **Multiple Payment Methods**: Cards, Bank transfers, USSD, etc.
- ✅ **Secure Processing**: PCI DSS compliant
- ✅ **Real-time Notifications**: Instant payment confirmations
- ✅ **Mobile Optimized**: Works on all devices
- ✅ **Multi-currency Support**: NGN, USD, GHS, ZAR, etc.

## M-Pesa Configuration (Fallback)

### 1. Register with Safaricom Developer Portal
1. Go to [https://developer.safaricom.co.ke/](https://developer.safaricom.co.ke/)
2. Create an account and log in
3. Create a new app to get your credentials

### 2. Get Your Credentials
You'll need the following from your Safaricom Developer account:
- **Consumer Key** (MPESA_CONSUMER_KEY)
- **Consumer Secret** (MPESA_CONSUMER_SECRET)
- **Business Short Code** (MPESA_SHORTCODE) - Use 174379 for sandbox
- **Pass Key** (MPESA_PASSKEY) - Use the sandbox passkey

### 3. Set Environment Variables
Create a `.env` file in your project root with:

```
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your-mpesa-passkey
MPESA_CALLBACK_URL=https://campus-shoppy-maseno.onrender.com
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
DJANGO_SECRET_KEY=django-insecure-your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## Testing Payment Flow
1. **Add items to cart**
2. **Proceed to checkout**
3. **Choose payment method** (Paystack is primary)
4. **Complete payment** using your preferred method
5. **Receive confirmation** and order details

## Production Features
- ✅ **Live Payment Processing**: Real money transactions
- ✅ **Secure Webhooks**: Payment verification
- ✅ **Order Management**: Complete order tracking
- ✅ **Email Notifications**: Customer confirmations
- ✅ **Mobile Responsive**: Works on all devices
