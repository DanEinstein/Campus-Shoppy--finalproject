# 🚀 Campus Shoppy - Production Deployment Guide

## ✅ **Pre-Deployment Checklist**

All critical security and functionality fixes have been implemented:

- ✅ **Cloudinary Integration** - Images will persist across deployments
- ✅ **Payment Amount Verification** - Prevents fraud attempts
- ✅ **Inventory Management** - Stock decrements on successful payment
- ✅ **Product Population Command** - Database can be populated with sample data
- ✅ **Security Hardening** - Debug views protected, logging configured
- ✅ **Missing Dependencies Added** - dj-database-url, cloudinary packages

---

## 📋 **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

**New Dependencies Added:**
- `dj-database-url>=0.5.0` - Database URL parsing
- `cloudinary>=1.36.0` - Cloudinary SDK
- `django-cloudinary-storage>=0.3.0` - Django Cloudinary integration

---

## 🔐 **Step 2: Configure Environment Variables**

### **For Local Development (.env file):**

Create a `.env` file in the project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-generate-new-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for local development)
DATABASE_URL=sqlite:///db.sqlite3

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# Paystack Configuration (Use TEST keys for development)
PAYSTACK_SECRET_KEY=sk_test_your_test_secret_key
PAYSTACK_PUBLIC_KEY=pk_test_your_test_public_key
PAYSTACK_CALLBACK_URL=http://localhost:8000/payments/paystack/callback/

# M-Pesa Configuration (Optional - for testing)
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_SHORTCODE=your_mpesa_shortcode
MPESA_PASSKEY=your_mpesa_passkey
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=http://localhost:8000/payments/callback/

# Security Settings (False for local development)
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### **For Production (Render.com Environment Variables):**

Add these in Render Dashboard → Environment:

```bash
SECRET_KEY=generate-a-new-strong-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com

# Database (Render provides this automatically for PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database

# Cloudinary Configuration (CRITICAL - Get from cloudinary.com)
CLOUDINARY_CLOUD_NAME=your_production_cloud_name
CLOUDINARY_API_KEY=your_production_api_key
CLOUDINARY_API_SECRET=your_production_api_secret

# Paystack Configuration (Use LIVE keys for production)
PAYSTACK_SECRET_KEY=sk_live_your_live_secret_key
PAYSTACK_PUBLIC_KEY=pk_live_your_live_public_key
PAYSTACK_CALLBACK_URL=https://your-app-name.onrender.com/payments/paystack/callback/

# M-Pesa Configuration (Use LIVE credentials for production)
MPESA_CONSUMER_KEY=your_live_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_live_mpesa_consumer_secret
MPESA_SHORTCODE=your_live_mpesa_shortcode
MPESA_PASSKEY=your_live_mpesa_passkey
MPESA_BASE_URL=https://api.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-app-name.onrender.com/payments/callback/

# Security Settings (MUST be True for production)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

---

## 🖼️ **Step 3: Setup Cloudinary**

### **Why Cloudinary is CRITICAL:**
- Render.com uses **ephemeral filesystem** - all uploaded files are deleted on each deployment
- Without Cloudinary, product images will disappear after every deployment
- Cloudinary provides permanent, CDN-backed image storage

### **Setup Instructions:**

1. **Create Cloudinary Account:**
   - Go to https://cloudinary.com/
   - Sign up for a free account (25GB storage, 25GB bandwidth/month)

2. **Get Your Credentials:**
   - Go to Dashboard
   - Copy: Cloud Name, API Key, API Secret
   - Add these to your environment variables

3. **Upload Product Images:**
   
   **Option A: Upload via Cloudinary Dashboard**
   - Go to Media Library
   - Create folder: `products`
   - Upload images
   - Copy the Public ID (e.g., `products/hoodie_maseno`)

   **Option B: Upload via Python Script**
   ```python
   import cloudinary.uploader
   
   result = cloudinary.uploader.upload(
       "path/to/local/image.jpg",
       public_id="products/hoodie_maseno",
       folder="products"
   )
   print(result['public_id'])  # Use this in populate_products.py
   ```

4. **Update Product Photo IDs:**
   - Edit `shop/management/commands/populate_products.py`
   - Replace placeholder IDs with your actual Cloudinary Public IDs
   - Format: `'products/image_name'` (no file extension)

---

## 🗄️ **Step 4: Database Setup**

### **Local Development:**

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate database with sample products
python manage.py populate_products

# Collect static files
python manage.py collectstatic --noinput
```

### **Production (Render.com):**

Add to your `render.yaml` or run manually after deployment:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py populate_products
python manage.py createsuperuser  # Create admin account
```

---

## 💳 **Step 5: Payment Gateway Setup**

### **Paystack (Primary Payment Gateway):**

1. **Create Paystack Account:**
   - Go to https://paystack.com/
   - Sign up for a business account
   - Complete KYC verification

2. **Get API Keys:**
   - Go to Settings → API Keys & Webhooks
   - Copy Test Keys (for development)
   - Copy Live Keys (for production)

3. **Configure Webhook:**
   - Webhook URL: `https://your-app.onrender.com/payments/paystack/callback/`
   - Events to subscribe: `charge.success`

4. **Test Payment:**
   - Use test card: `4084084084084081`
   - CVV: `408`
   - Expiry: Any future date
   - PIN: `0000`
   - OTP: `123456`

### **M-Pesa (Optional Fallback):**

1. **Register on Safaricom Daraja:**
   - Go to https://developer.safaricom.co.ke/
   - Create account and register app

2. **Get Credentials:**
   - Consumer Key
   - Consumer Secret
   - Shortcode
   - Passkey

3. **Configure Callback URL:**
   - `https://your-app.onrender.com/payments/callback/`

---

## 🌐 **Step 6: Deploy to Render.com**

### **Method 1: Using render.yaml (Recommended)**

Your `render.yaml` is already configured. Just:

1. Push code to GitHub
2. Connect repository to Render
3. Render will auto-deploy using `render.yaml`

### **Method 2: Manual Configuration**

1. **Create Web Service:**
   - Go to Render Dashboard
   - New → Web Service
   - Connect GitHub repository

2. **Configure Build Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn django_ecommerce.wsgi:application`

3. **Add Environment Variables:**
   - Add all variables from Step 2 (Production section)

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete

---

## ✅ **Step 7: Post-Deployment Verification**

### **1. Check Application Health:**
```bash
curl https://your-app.onrender.com/health/
```

### **2. Verify Cloudinary Integration:**
- Upload a product image via Django admin
- Check if image URL starts with `https://res.cloudinary.com/`
- Verify image loads correctly

### **3. Test Payment Flow:**
- Add product to cart
- Proceed to checkout
- Complete payment with test card
- Verify:
  - ✅ Payment status updates to "success"
  - ✅ Order marked as paid
  - ✅ Inventory decremented
  - ✅ Cart cleared

### **4. Check Logs:**
```bash
# On Render Dashboard
Logs → View Logs

# Look for:
- No errors during startup
- Cloudinary connection successful
- Database migrations applied
```

---

## 🔒 **Security Checklist**

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` (never commit to git)
- ✅ `SESSION_COOKIE_SECURE=True`
- ✅ `CSRF_COOKIE_SECURE=True`
- ✅ HTTPS enforced (Render does this automatically)
- ✅ Payment amount verification implemented
- ✅ Debug views protected
- ✅ Logging configured
- ✅ `.env` file in `.gitignore`

---

## 🐛 **Troubleshooting**

### **Images Not Loading:**
```python
# Check Cloudinary configuration
python manage.py shell
>>> from django.conf import settings
>>> print(settings.CLOUDINARY_STORAGE)
>>> print(settings.DEFAULT_FILE_STORAGE)
```

### **Payment Verification Failing:**
```python
# Check Paystack credentials
>>> print(settings.PAYSTACK_SECRET_KEY[:10])  # Should start with sk_
>>> print(settings.PAYSTACK_PUBLIC_KEY[:10])  # Should start with pk_
```

### **Database Errors:**
```bash
# Reset database (DEVELOPMENT ONLY!)
python manage.py flush
python manage.py migrate
python manage.py populate_products
```

### **Static Files Not Loading:**
```bash
python manage.py collectstatic --noinput --clear
```

---

## 📊 **Performance Optimization**

### **1. Enable Database Connection Pooling:**
Already configured in `settings.py`:
```python
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600  # ✅ Connection pooling enabled
    )
}
```

### **2. Use Cloudinary Transformations:**
```html
<!-- Optimize images on-the-fly -->
<img src="{{ product.photo.url }}?w=400&h=400&c_fill&q_auto&f_auto" alt="{{ product.name }}">
```

### **3. Enable Caching (Future Enhancement):**
```python
# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## 📈 **Monitoring & Maintenance**

### **1. Monitor Payment Logs:**
```bash
# Check logs/django.log for payment fraud attempts
grep "PAYMENT FRAUD ATTEMPT" logs/django.log
```

### **2. Monitor Inventory:**
```python
# Check products with low inventory
python manage.py shell
>>> from shop.models import Product
>>> Product.objects.filter(inventory__lt=10)
```

### **3. Backup Database:**
```bash
# For PostgreSQL on Render
pg_dump $DATABASE_URL > backup.sql
```

---

## 🎉 **Success Criteria**

Your application is production-ready when:

- ✅ All environment variables configured
- ✅ Cloudinary images loading correctly
- ✅ Test payment completes successfully
- ✅ Inventory decrements after payment
- ✅ No errors in logs
- ✅ HTTPS enabled
- ✅ Admin panel accessible
- ✅ Products visible on homepage

---

## 📞 **Support & Resources**

- **Django Documentation:** https://docs.djangoproject.com/
- **Cloudinary Docs:** https://cloudinary.com/documentation/django_integration
- **Paystack Docs:** https://paystack.com/docs/api/
- **Render Docs:** https://render.com/docs

---

## 🚨 **CRITICAL NOTES**

1. **Never commit `.env` file to git** - It contains sensitive credentials
2. **Always use LIVE keys in production** - Test keys won't process real payments
3. **Backup database before major changes** - Prevent data loss
4. **Monitor payment logs regularly** - Detect fraud attempts early
5. **Keep Django and dependencies updated** - Security patches

---

**Deployment Date:** {{ deployment_date }}
**Version:** 1.0.0
**Status:** ✅ Production Ready
