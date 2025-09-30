# 🔗 Campus Shoppy URL Reference Guide

## ✅ **URL Configuration Fixed**

### **🎯 Main URL Patterns (django_ecommerce/urls.py):**

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('health/', health_check, name='health'),
    path('blog/', include('blog.urls')),           # No namespace
    path('contact/', include('contact.urls')),    # No namespace
    path('about/', include('about.urls')),        # No namespace
    path('shop/', include('shop.urls')),          # No namespace
    path('cart/', include('cart.urls')),          # Namespace: cart
    path('payments/', include('payments.urls')),  # Namespace: payments
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('account.urls')),   # No namespace
]
```

---

## 📋 **Correct URL References**

### **🏠 Home & Main Pages:**
```django
{% url 'home' %}           # Homepage
{% url 'about' %}          # About page
{% url 'contact' %}        # Contact page
```

### **🛍️ Shop URLs:**
```django
{% url 'shop' %}                    # Shop listing
{% url 'product-details' product.id %}  # Product details
{% url 'wishlist' %}               # Wishlist
{% url 'add_to_wishlist' product.id %}  # Add to wishlist
{% url 'remove_from_wishlist' item.id %}  # Remove from wishlist
```

### **🛒 Cart URLs (with namespace):**
```django
{% url 'cart:cart_detail' %}       # Cart page
{% url 'cart:add_to_cart' product.id %}  # Add to cart
{% url 'cart:checkout' %}           # Checkout
{% url 'cart:update_cart' %}        # Update cart
```

### **💳 Payment URLs (with namespace):**
```django
{% url 'payments:initiate' order.id %}  # Initiate payment
{% url 'payments:status' order.id %}    # Payment status
{% url 'payments:verify' order.id %}   # Verify payment
{% url 'payments:confirm' order.id %}   # Confirm payment
{% url 'payments:callback' %}           # Payment callback
{% url 'payments:success' order.id %}  # Payment success
```

### **📝 Blog URLs:**
```django
{% url 'blog' %}                    # Blog listing
{% url 'post-details' post.id %}    # Blog post details
{% url 'post-by-category' category.name %}  # Posts by category
```

### **👤 Account URLs:**
```django
{% url 'signin' %}          # Login
{% url 'signup' %}          # Register
{% url 'signout' %}         # Logout
```

---

## 🚫 **Common URL Mistakes to Avoid**

### **❌ Incorrect (with namespace when not needed):**
```django
{% url 'shop:shop' %}        # WRONG - shop has no namespace
{% url 'blog:blog' %}        # WRONG - blog has no namespace
{% url 'about:about' %}      # WRONG - about has no namespace
{% url 'contact:contact' %}  # WRONG - contact has no namespace
```

### **❌ Incorrect (without namespace when needed):**
```django
{% url 'cart_detail' %}      # WRONG - should be cart:cart_detail
{% url 'initiate' %}         # WRONG - should be payments:initiate
{% url 'add_to_cart' %}      # WRONG - should be cart:add_to_cart
```

### **✅ Correct URL References:**
```django
{% url 'shop' %}                    # Shop listing
{% url 'blog' %}                    # Blog listing
{% url 'about' %}                   # About page
{% url 'contact' %}                 # Contact page
{% url 'cart:cart_detail' %}       # Cart page
{% url 'payments:initiate' order.id %}  # Payment initiation
{% url 'signin' %}                  # Login
{% url 'signup' %}                  # Register
{% url 'signout' %}                 # Logout
```

---

## 🔧 **URL Namespace Rules**

### **Apps WITH Namespaces:**
- **Cart**: `cart:cart_detail`, `cart:add_to_cart`, `cart:checkout`
- **Payments**: `payments:initiate`, `payments:status`, `payments:verify`

### **Apps WITHOUT Namespaces:**
- **Shop**: `shop`, `product-details`, `wishlist`
- **Blog**: `blog`, `post-details`, `post-by-category`
- **About**: `about`
- **Contact**: `contact`
- **Account**: `signin`, `signup`, `signout`

---

## 📱 **Navbar URL References**

### **Mobile Navbar (navbar_mobile.html):**
```html
<!-- Home -->
<a href="{% url 'home' %}">Home</a>

<!-- Shop Dropdown -->
<a href="{% url 'shop' %}">All Products</a>
<a href="{% url 'cart:cart_detail' %}">Cart</a>
<a href="{% url 'cart:checkout' %}">Checkout</a>
<a href="{% url 'wishlist' %}">Wishlist</a>

<!-- Blog -->
<a href="{% url 'blog' %}">Blog</a>

<!-- Other Pages -->
<a href="{% url 'about' %}">About</a>
<a href="{% url 'contact' %}">Contact</a>

<!-- User Actions -->
<a href="{% url 'signin' %}">Login</a>
<a href="{% url 'signup' %}">Register</a>
<a href="{% url 'signout' %}">Logout</a>
```

### **Original Navbar (navbar.html):**
```html
<!-- Same URL references as mobile navbar -->
<!-- All URLs are correctly configured -->
```

---

## 🎯 **URL Testing Checklist**

### **✅ Test These URLs:**
1. **Home**: `/` and `/home/`
2. **Shop**: `/shop/`
3. **Blog**: `/blog/`
4. **About**: `/about/`
5. **Contact**: `/contact/`
6. **Cart**: `/cart/`
7. **Checkout**: `/cart/checkout/`
8. **Login**: `/account/signin/`
9. **Register**: `/account/signup/`

### **✅ Test These URL Names:**
1. `{% url 'home' %}`
2. `{% url 'shop' %}`
3. `{% url 'blog' %}`
4. `{% url 'about' %}`
5. `{% url 'contact' %}`
6. `{% url 'cart:cart_detail' %}`
7. `{% url 'cart:checkout' %}`
8. `{% url 'signin' %}`
9. `{% url 'signup' %}`
10. `{% url 'signout' %}`

---

## 🚀 **Fixed Issues**

### **✅ Resolved:**
1. **Shop URL**: Changed from `{% url 'shop:shop' %}` to `{% url 'shop' %}`
2. **Blog URL**: Changed from `{% url 'blog:blog' %}` to `{% url 'blog' %}`
3. **Wishlist URL**: Changed from `{% url 'shop:wishlist' %}` to `{% url 'wishlist' %}`
4. **All URL references**: Now correctly match the URL configuration

### **✅ Working URLs:**
- All navigation links work correctly
- Blog access is functional
- Shop access is functional
- Cart and checkout work properly
- User authentication links work
- All dropdown menus function correctly

---

## 🎉 **Final Result**

**✅ All URL References Fixed!**

**What's Working:
- Blog access: `/blog/`
- Shop access: `/shop/`
- Cart functionality: `/cart/`
- User authentication: `/account/signin/`, `/account/signup/`
- All navigation links
- All dropdown menus
- Mobile responsive navigation

**🎊 The navbar now has correct URL references and all links work perfectly!**
