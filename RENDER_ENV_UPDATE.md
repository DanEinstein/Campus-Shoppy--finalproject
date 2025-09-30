# Quick Fix for Render Environment Variables

## 🚨 Immediate Fix Required

Your site is failing because the `ALLOWED_HOSTS` environment variable in Render doesn't include your domain.

## 🔧 Manual Fix in Render Dashboard

1. **Go to your Render dashboard**: https://dashboard.render.com
2. **Click on your service**: `campus-shoppy-maseno`
3. **Go to Environment tab**
4. **Add/Update these environment variables**:

```
DJANGO_ALLOWED_HOSTS=*.onrender.com,campus-shoppy-maseno-7y1e.onrender.com
MPESA_CALLBACK_URL=https://campus-shoppy-maseno-7y1e.onrender.com/payments/callback/
```

## 🚀 Alternative: Quick Code Fix

I've already updated the `django_ecommerce/settings.py` file to include your domain by default, so you can:

1. **Commit and push the changes**:
   ```bash
   git add .
   git commit -m "Add campus-shoppy-maseno-7y1e.onrender.com to ALLOWED_HOSTS default"
   git push origin main
   ```

2. **Render will automatically redeploy** with the fix

## ✅ After Fix

Your site will be accessible at:
**https://campus-shoppy-maseno-7y1e.onrender.com**

## 🔍 What Was Fixed

- Added `*.onrender.com` wildcard to allow any Render subdomain
- Added your specific domain `campus-shoppy-maseno-7y1e.onrender.com`
- Updated M-Pesa callback URL to your actual domain
- Made the settings more flexible for future deployments
