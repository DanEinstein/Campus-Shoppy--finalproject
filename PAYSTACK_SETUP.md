# Paystack Environment Variables Setup

## For Local Development
Create a `.env` file in your project root with the following variables:

```bash
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Paystack Configuration (Live)
PAYSTACK_SECRET_KEY=your-paystack-secret-key-here
PAYSTACK_PUBLIC_KEY=your-paystack-public-key-here
PAYSTACK_CALLBACK_URL=https://campus-shoppy-maseno.onrender.com/payments/paystack/callback/

# M-Pesa Configuration (Fallback)
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your-mpesa-passkey
MPESA_CALLBACK_URL=https://campus-shoppy-maseno.onrender.com/payments/callback/
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
```

## For Production Deployment (Render.com)

### 1. Set Environment Variables in Render Dashboard:
1. Go to your Render dashboard
2. Navigate to your service
3. Go to "Environment" tab
4. Add the following environment variables:

```
PAYSTACK_SECRET_KEY=your-paystack-secret-key-here
PAYSTACK_PUBLIC_KEY=your-paystack-public-key-here
PAYSTACK_CALLBACK_URL=https://campus-shoppy-maseno.onrender.com/payments/paystack/callback/
```

### 2. Security Notes:
- ✅ **Never commit API keys to Git
- ✅ **Use environment variables for all sensitive data
- ✅ **Keep your `.env` file in `.gitignore`
- ✅ **Use different keys for development and production

## Testing the Integration

### 1. Local Testing:
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp PAYSTACK_SETUP.md .env
# Edit .env with your actual values

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### 2. Production Testing:
1. Deploy to Render with environment variables set
2. Test payment flow with real Paystack integration
3. Verify webhook callbacks are working
4. Test with small amounts first

## Payment Flow Testing

### Test Cards (Paystack Test Mode):
- **Successful Payment**: 4084084084084081
- **Declined Payment**: 4084084084084085
- **Insufficient Funds**: 4084084084084082

### Test Bank Account:
- **Bank**: Access Bank
- **Account**: 0001234567
- **Amount**: Any amount

## Security Best Practices

1. **Environment Variables**: Always use environment variables for API keys
2. **Webhook Verification**: Verify Paystack webhook signatures
3. **HTTPS Only**: Ensure all payment pages use HTTPS
4. **Input Validation**: Validate all payment data
5. **Error Handling**: Implement proper error handling for failed payments

## Troubleshooting

### Common Issues:
1. **"Invalid API Key"**: Check your PAYSTACK_SECRET_KEY
2. **"Webhook not working"**: Verify PAYSTACK_CALLBACK_URL
3. **"Payment not completing"**: Check browser console for JavaScript errors
4. **"Amount mismatch"**: Ensure amount is in kobo (multiply by 100)

### Support:
- Paystack Documentation: https://paystack.com/docs
- Paystack Support: support@paystack.com
- Campus Shoppy Support: abrisonscreatives.agency@gmail.com
