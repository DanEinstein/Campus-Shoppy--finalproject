# 🚀 Quick Deployment Commands

## Step 1: Commit and Push the Fix

```bash
git add .
git commit -m "Fix: Add Order model import to cart views - Resolves NoReverseMatch deployment error"
git push origin main
```

## Step 2: Monitor Render Deployment

1. Go to your Render dashboard: https://dashboard.render.com
2. Find your "Campus Shoppy" service
3. Watch the build logs
4. Wait for "Deploy succeeded" message

## Step 3: Run Post-Deployment Commands (in Render Shell)

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations (if any pending)
python manage.py migrate

# Verify deployment
python manage.py check --deploy
```

## Step 4: Test the Application

Visit these URLs to verify everything works:

1. **Homepage**: https://campus-shoppy-maseno.onrender.com/
2. **Health Check**: https://campus-shoppy-maseno.onrender.com/health/
3. **Shop**: https://campus-shoppy-maseno.onrender.com/shop/
4. **Cart**: https://campus-shoppy-maseno.onrender.com/cart/
5. **Admin**: https://campus-shoppy-maseno.onrender.com/admin/

## Step 5: Test Complete Checkout Flow

1. Add a product to cart
2. Go to cart
3. Click "Proceed to Checkout"
4. Fill in billing details
5. Submit order
6. Verify redirect to Paystack payment page
7. Complete test payment
8. Verify order is marked as paid

## 🔧 If Issues Persist

### Check Render Logs
```bash
# In Render dashboard, click "Logs" tab
# Look for any Python errors or tracebacks
```

### Common Issues

**Issue**: Static files not loading
```bash
# Solution: Run collectstatic
python manage.py collectstatic --noinput
```

**Issue**: Database errors
```bash
# Solution: Run migrations
python manage.py migrate
```

**Issue**: Environment variables not set
```bash
# Solution: Check Render Environment Variables
# Go to: Dashboard → Your Service → Environment
# Verify all required variables are set
```

## 📋 Required Environment Variables

Make sure these are set in Render:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=campus-shoppy-maseno.onrender.com`
- `DATABASE_URL` (auto-set by Render if using their DB)
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `PAYSTACK_SECRET_KEY`
- `PAYSTACK_PUBLIC_KEY`
- `PAYSTACK_CALLBACK_URL=https://campus-shoppy-maseno.onrender.com/payments/paystack/callback/`
- `CSRF_TRUSTED_ORIGINS=https://campus-shoppy-maseno.onrender.com`

## ✅ Success Indicators

You'll know deployment succeeded when:
- ✅ Build completes without errors
- ✅ Homepage loads correctly
- ✅ Can add products to cart
- ✅ Checkout redirects to payment page (not error page)
- ✅ No "NoReverseMatch" errors in logs

---

**Ready to deploy!** Just run the git commands above and Render will handle the rest.
