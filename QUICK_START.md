# 🚀 Campus Shoppy - Quick Start Guide

## ⚡ **5-Minute Setup**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Environment**
Create `.env` file:
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your credentials:
# - SECRET_KEY (generate new one)
# - CLOUDINARY credentials
# - PAYSTACK keys
```

### **3. Setup Database**
```bash
python manage.py migrate
python manage.py populate_products
python manage.py createsuperuser
```

### **4. Run Server**
```bash
python manage.py runserver
```

Visit: http://localhost:8000

---

## 🔑 **Essential Commands**

### **Development:**
```bash
# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Populate sample products
python manage.py populate_products

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

### **Testing:**
```bash
# Test payment flow
# 1. Add product to cart
# 2. Checkout
# 3. Use test card: 4084084084084081

# Check logs
tail -f logs/django.log
```

---

## 🌐 **Quick Deploy to Render**

### **1. Push to GitHub:**
```bash
git add .
git commit -m "Production ready deployment"
git push origin main
```

### **2. On Render Dashboard:**
- New → Web Service
- Connect GitHub repo
- Add environment variables from `.env.example`
- Deploy

### **3. Post-Deployment:**
```bash
# SSH into Render or use dashboard console
python manage.py migrate
python manage.py populate_products
python manage.py createsuperuser
```

---

## 📋 **Environment Variables Checklist**

**Required for Production:**
- ✅ `SECRET_KEY` - Django secret key
- ✅ `DEBUG=False` - Disable debug mode
- ✅ `ALLOWED_HOSTS` - Your domain
- ✅ `CLOUDINARY_CLOUD_NAME` - From cloudinary.com
- ✅ `CLOUDINARY_API_KEY` - From cloudinary.com
- ✅ `CLOUDINARY_API_SECRET` - From cloudinary.com
- ✅ `PAYSTACK_SECRET_KEY` - From paystack.com
- ✅ `PAYSTACK_PUBLIC_KEY` - From paystack.com
- ✅ `DATABASE_URL` - Auto-provided by Render

**Optional:**
- ⚪ M-Pesa credentials (if using M-Pesa)

---

## 🐛 **Quick Troubleshooting**

### **Images not loading?**
```bash
# Check Cloudinary config
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEFAULT_FILE_STORAGE)
# Should be: 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### **Payment failing?**
```bash
# Check Paystack keys
>>> print(settings.PAYSTACK_SECRET_KEY[:10])
# Should start with: sk_test_ or sk_live_
```

### **Database errors?**
```bash
# Reset database (DEVELOPMENT ONLY!)
python manage.py flush
python manage.py migrate
python manage.py populate_products
```

---

## 📚 **Documentation**

- **Full Deployment Guide:** See `DEPLOYMENT_GUIDE.md`
- **Implementation Details:** See `IMPLEMENTATION_SUMMARY.md`
- **Django Docs:** https://docs.djangoproject.com/

---

## ✅ **Production Checklist**

Before going live:
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] Cloudinary configured
- [ ] Paystack LIVE keys configured
- [ ] HTTPS enabled (automatic on Render)
- [ ] Database backed up
- [ ] Test payment completed successfully
- [ ] Admin account created

---

## 🎉 **You're Ready!**

Your Campus Shoppy platform is production-ready with:
- ✅ Secure payment processing
- ✅ Cloudinary image storage
- ✅ Inventory management
- ✅ Fraud prevention
- ✅ Professional logging

**Need help?** Check `DEPLOYMENT_GUIDE.md` for detailed instructions.
