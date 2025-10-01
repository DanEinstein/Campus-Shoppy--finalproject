# 🏫 Campus Shoppy - E-commerce Platform

A comprehensive e-commerce platform built for Maseno University students, featuring a modern carousel, secure payments, and mobile-optimized design.

## ✨ Features

### 🎠 **Working Carousel**
- ✅ **Auto-advancing slides** with 5-second intervals
- ✅ **Touch/swipe support** for mobile devices
- ✅ **Navigation controls** (arrows and dots)
- ✅ **Responsive design** for all screen sizes
- ✅ **No scroll interference** on mobile

### 💳 **Payment System**
- ✅ **M-Pesa integration** for Kenyan payments
- ✅ **Secure payment processing** with callback handling
- ✅ **Payment verification** and status tracking
- ✅ **Manual payment confirmation** as fallback
- ✅ **Order management** with payment status

### 🛒 **Shopping Cart**
- ✅ **Add/remove products** from cart
- ✅ **Quantity management** with real-time updates
- ✅ **Session-based cart** for non-logged users
- ✅ **User-specific cart** for logged-in users
- ✅ **Checkout process** with order creation

### 📱 **Mobile Optimization**
- ✅ **Responsive design** for all devices
- ✅ **Touch-friendly interface** with proper spacing
- ✅ **Mobile carousel** with swipe gestures
- ✅ **Optimized navigation** for small screens
- ✅ **Fast loading** with optimized assets

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Setup Database**
```bash
python manage.py migrate
python manage.py collectstatic
```

### **3. Create Superuser**
```bash
python manage.py createsuperuser
```

### **4. Run Server**
```bash
# Use the stable server script
python start_server.py

# Or use the batch file
run_server_stable.bat

# Or manual command
python manage.py runserver 127.0.0.1:8000 --noreload --insecure
```

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file with:
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,*.onrender.com

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-domain.com/payments/callback/
```

## 📁 Project Structure

```
Campus Shoppy/
├── django_ecommerce/          # Main Django project
├── templates/                 # HTML templates
│   ├── home.html             # Main homepage with carousel
│   ├── base/                 # Base templates
│   └── payments/             # Payment templates
├── static/                   # Static files (CSS, JS, images)
├── shop/                     # Product management
├── cart/                     # Shopping cart functionality
├── payments/                 # M-Pesa payment integration
├── account/                  # User authentication
├── blog/                     # Blog system
├── contact/                  # Contact forms
└── about/                    # About page
```

## 🎯 Key Components

### **Carousel Implementation**
- **HTML**: Clean structure with inline styles for reliability
- **JavaScript**: Simple, conflict-free carousel logic
- **CSS**: Responsive design with mobile optimization
- **Touch Support**: Swipe gestures for mobile navigation

### **Payment System**
- **M-Pesa STK Push**: Direct mobile payment integration
- **Callback Handling**: Automatic payment confirmation
- **Manual Verification**: Fallback for API issues
- **Order Tracking**: Complete payment status management

### **Cart System**
- **Session Management**: Persistent cart across sessions
- **User Integration**: User-specific cart for logged-in users
- **Real-time Updates**: Dynamic cart updates without page refresh
- **Checkout Process**: Seamless order creation and payment

## 🚀 Deployment

### **Render.com Deployment**
1. **Connect Repository**: Link your GitHub repository
2. **Set Environment Variables**: Add all required environment variables
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn django_ecommerce.wsgi:application`
5. **Static Files**: Run `python manage.py collectstatic`

### **Environment Variables for Production**
```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_ALLOWED_HOSTS=your-domain.com,*.onrender.com
MPESA_BASE_URL=https://api.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-domain.com/payments/callback/
```

## 🔍 Testing

### **Test Carousel**
1. Visit homepage - carousel should display immediately
2. Test navigation arrows and dots
3. Test auto-advance (5-second intervals)
4. Test mobile swipe gestures

### **Test Payments**
1. Add products to cart
2. Proceed to checkout
3. Enter phone number for M-Pesa
4. Complete payment process
5. Verify payment status

### **Test Mobile**
1. Open on mobile device
2. Test carousel swipe gestures
3. Test navigation and forms
4. Verify responsive design

## 🛠️ Troubleshooting

### **Carousel Not Displaying**
- Check browser console for JavaScript errors
- Verify images exist in `static/images/`
- Run `python manage.py collectstatic`
- Try the backup simple carousel implementation

### **Payment Issues**
- Verify M-Pesa credentials in environment variables
- Check callback URL is accessible
- Test with sandbox credentials first
- Use manual verification as fallback

### **Database Issues**
- Run `python manage.py migrate`
- Check database connection
- Verify all models are properly defined
- Run `python manage.py makemigrations` if needed

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the deployment checklist
3. Verify all environment variables are set
4. Test with the stable server scripts provided

## 🎉 Success Indicators

When everything is working correctly, you should see:
- ✅ **Carousel displays immediately** on homepage
- ✅ **Smooth slide transitions** with auto-advance
- ✅ **Working navigation** (arrows, dots, swipe)
- ✅ **Mobile-optimized** carousel and navigation
- ✅ **Payment system** processes M-Pesa payments
- ✅ **Cart functionality** adds/removes products
- ✅ **Responsive design** works on all devices

The platform is now ready for deployment and production use! 🚀