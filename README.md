# 🏫 Campus Shoppy - E-commerce Platform

A comprehensive, production-ready e-commerce platform built specifically for Maseno University students. Features modern design, secure payment processing, and mobile-optimized shopping experience.

## 🌟 **Live Demo**
**🚀 [Visit Campus Shoppy](https://campus-shoppy-maseno-7y1e.onrender.com/)**

## ✨ **Key Features**

### 🎠 **Modern Homepage**
- ✅ **Auto-advancing carousel** with 5-second intervals
- ✅ **Touch/swipe support** for mobile devices
- ✅ **Navigation controls** (arrows and dots)
- ✅ **Responsive design** for all screen sizes
- ✅ **Multiple homepage templates** (beautiful, minimal, mobile-optimized)

### 💳 **Payment Integration**
- ✅ **Paystack (Primary)**: Live payment processing with Kenyan Shilling (KES)
- ✅ **M-Pesa (Fallback)**: STK Push integration for mobile payments
- ✅ **Multiple Payment Methods**: Cards, Bank transfers, USSD, etc.
- ✅ **Secure Processing**: PCI DSS compliant payment handling
- ✅ **Real-time Verification**: Webhook-based payment confirmation
- ✅ **Cart Auto-Clear**: Automatic cart clearing on successful payment

### 🛒 **E-commerce Functionality**
- ✅ **Product Management**: Full CRUD operations for products
- ✅ **Category System**: Organized product categorization
- ✅ **Shopping Cart**: Session-based cart with real-time updates
- ✅ **Wishlist**: Save favorite products for later
- ✅ **Product Search**: Find products easily
- ✅ **Order Management**: Complete order tracking system

### 👤 **User Management**
- ✅ **User Registration**: Seamless account creation with auto-login
- ✅ **Authentication**: Secure login/logout with proper redirects
- ✅ **User Profiles**: Personalized shopping experience
- ✅ **Session Management**: Persistent cart across sessions

### 📝 **Content Management**
- ✅ **Blog System**: Full blog with categories and tags
- ✅ **About Page**: Comprehensive platform information
- ✅ **Contact Forms**: User communication system
- ✅ **Newsletter**: Email subscription functionality

### 📱 **Mobile Optimization**
- ✅ **Responsive Design**: Mobile-first approach
- ✅ **Touch-Friendly Interface**: Optimized for touch interactions
- ✅ **Fast Loading**: Optimized assets and performance
- ✅ **Cross-Device Compatibility**: Works on all devices

## 🛠️ **Technology Stack**

### **Backend**
- **Django 3.1.14**: Python web framework
- **SQLite**: Development database (PostgreSQL ready for production)
- **Django ORM**: Database abstraction layer
- **Django REST Framework**: API development ready

### **Frontend**
- **Bootstrap 5**: Responsive CSS framework
- **JavaScript**: Interactive carousel and cart functionality
- **HTML5/CSS3**: Modern web standards
- **Font Awesome**: Icon library

### **Payment Processing**
- **Paystack**: Primary payment gateway (Live integration)
- **M-Pesa Daraja API**: Mobile payment integration
- **Webhook Handling**: Real-time payment verification

### **Deployment**
- **Render.com**: Cloud hosting platform
- **Gunicorn**: WSGI HTTP server
- **WhiteNoise**: Static file serving
- **Environment Variables**: Secure configuration

## 🚀 **Quick Start**

### **1. Clone Repository**
```bash
git clone https://github.com/DanEinstein/Campus-Shoppy--finalproject.git
cd Campus-Shoppy--finalproject
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Setup Database**
```bash
python manage.py migrate
python manage.py collectstatic
```

### **4. Create Superuser**
```bash
python manage.py createsuperuser
```

### **5. Run Development Server**
```bash
python manage.py runserver
```

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file with:
```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,*.onrender.com

# Paystack Configuration (Primary)
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_CALLBACK_URL=https://your-domain.com/payments/paystack/callback/

# M-Pesa Configuration (Fallback)
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-domain.com/payments/callback/
```

## 📁 **Project Structure**

```
Campus Shoppy/
├── django_ecommerce/          # Main Django project
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration
├── templates/                 # HTML templates
│   ├── home.html             # Main homepage with carousel
│   ├── base/                 # Base templates
│   ├── shop/                 # Product templates
│   ├── cart/                 # Shopping cart templates
│   ├── payments/             # Payment templates
│   ├── account/              # Authentication templates
│   ├── blog/                 # Blog templates
│   └── contact/              # Contact templates
├── static/                   # Static files (CSS, JS, images)
│   ├── css/                  # Custom stylesheets
│   ├── js/                   # JavaScript files
│   └── images/               # Image assets
├── shop/                     # Product management app
│   ├── models.py             # Product and Category models
│   ├── views.py              # Product views
│   └── urls.py               # Shop URL patterns
├── cart/                     # Shopping cart functionality
│   ├── models.py             # Order and OrderItem models
│   ├── views.py              # Cart views
│   └── cart.py               # Cart session management
├── payments/                 # Payment integration
│   ├── models.py             # Payment model
│   ├── views.py              # M-Pesa payment views
│   └── paystack_views.py     # Paystack payment views
├── account/                  # User authentication
│   ├── models.py             # User models
│   ├── views.py              # Authentication views
│   └── forms.py              # Custom forms
├── blog/                     # Blog system
│   ├── models.py             # Blog models
│   └── views.py              # Blog views
├── contact/                  # Contact forms
├── about/                    # About page
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment config
├── Procfile                 # Process configuration
└── runtime.txt              # Python version
```

## 🎯 **Key Components**

### **Homepage Carousel**
- **HTML**: Clean structure with inline styles for reliability
- **JavaScript**: Simple, conflict-free carousel logic
- **CSS**: Responsive design with mobile optimization
- **Touch Support**: Swipe gestures for mobile navigation
- **Auto-advance**: 5-second intervals with pause on hover

### **Payment System**
- **Paystack Integration**: Live payment processing with KES currency
- **M-Pesa STK Push**: Direct mobile payment integration
- **Webhook Handling**: Real-time payment verification
- **Manual Verification**: Fallback for API issues
- **Order Tracking**: Complete payment status management

### **Shopping Cart**
- **Session Management**: Persistent cart across sessions
- **User Integration**: User-specific cart for logged-in users
- **Real-time Updates**: Dynamic cart updates without page refresh
- **Checkout Process**: Seamless order creation and payment
- **Cart Clearing**: Automatic cart clearing on successful payment

## 🚀 **Deployment**

### **Render.com Deployment (Current)**
The application is currently deployed on Render.com with the following configuration:

1. **Repository**: Connected to GitHub repository
2. **Environment Variables**: Configured for production
3. **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate`
4. **Start Command**: `gunicorn django_ecommerce.wsgi:application --bind 0.0.0.0:$PORT`
5. **Static Files**: Handled by WhiteNoise middleware

### **Production Environment Variables**
```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_ALLOWED_HOSTS=campus-shoppy-maseno-7y1e.onrender.com,*.onrender.com
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
PAYSTACK_CALLBACK_URL=https://campus-shoppy-maseno-7y1e.onrender.com/payments/paystack/callback/
```

## 🔍 **Testing**

### **Live Testing**
1. **Visit Homepage**: [https://campus-shoppy-maseno-7y1e.onrender.com/](https://campus-shoppy-maseno-7y1e.onrender.com/)
2. **Test Carousel**: Auto-advancing slides with navigation
3. **Test Mobile**: Swipe gestures and responsive design
4. **Test Payments**: Complete checkout process with Paystack
5. **Test Cart**: Add/remove products and checkout flow

### **Local Testing**
```bash
# Run development server
python manage.py runserver

# Test carousel functionality
# Test payment integration
# Test mobile responsiveness
```

## 🛠️ **Troubleshooting**

### **Common Issues**
- **Carousel Not Displaying**: Check browser console for JavaScript errors
- **Payment Issues**: Verify Paystack credentials in environment variables
- **Database Issues**: Run `python manage.py migrate`
- **Static Files**: Run `python manage.py collectstatic`

### **Development Issues**
- **Import Errors**: Ensure all dependencies are installed
- **URL Errors**: Check URL patterns and namespacing
- **Template Errors**: Verify template inheritance and context variables

## 📊 **Performance Metrics**

### **Technical Performance**
- ✅ **Fast Loading**: Optimized static files and database queries
- ✅ **Mobile Performance**: Touch-optimized interactions
- ✅ **Cross-Browser**: Compatible with major browsers
- ✅ **Responsive**: Works on all device sizes

### **Business Metrics**
- ✅ **Conversion Ready**: Complete checkout flow
- ✅ **Payment Success**: Multiple payment methods
- ✅ **User Retention**: Account system and wishlist
- ✅ **Mobile Commerce**: Mobile-optimized experience

## 🎯 **Key Achievements**

1. **🎓 Student-Focused**: Designed specifically for Maseno University students
2. **💳 Payment Ready**: Live Paystack integration with KES currency
3. **📱 Mobile-First**: Optimized for mobile commerce
4. **🔒 Secure**: Proper security measures and credential management
5. **🚀 Production Ready**: Fully deployed and functional
6. **🎨 Professional**: Modern, clean design
7. **⚡ Fast**: Optimized performance and loading

## 🎉 **Success Indicators**

When everything is working correctly, you should see:
- ✅ **Carousel displays immediately** on homepage
- ✅ **Smooth slide transitions** with auto-advance
- ✅ **Working navigation** (arrows, dots, swipe)
- ✅ **Mobile-optimized** carousel and navigation
- ✅ **Payment system** processes payments successfully
- ✅ **Cart functionality** adds/removes products
- ✅ **Responsive design** works on all devices

## 📞 **Support & Contributing**

### **Issues & Questions**
1. Check the troubleshooting section above
2. Review the deployment checklist
3. Verify all environment variables are set
4. Test with the stable server scripts provided

### **Contributing**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🏆 **Project Status**

**✅ PRODUCTION READY** - The Campus Shoppy platform is fully functional, deployed, and ready for business! 🚀

**Live Demo**: [https://campus-shoppy-maseno-7y1e.onrender.com/](https://campus-shoppy-maseno-7y1e.onrender.com/)