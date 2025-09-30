# Campus Shoppy - E-commerce Platform

A Django-based e-commerce platform with M-Pesa payment integration for Kenyan students.

## Features

- 🛒 **Product Catalog** - Browse and search products
- 🛍️ **Shopping Cart** - Add/remove items, quantity management
- 💳 **M-Pesa Payments** - STK Push integration with payment verification
- 👤 **User Authentication** - Sign up, sign in, user profiles
- 📱 **Responsive Design** - Mobile-friendly interface
- 🔒 **Secure** - Environment-based configuration, CSRF protection

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd campus-shoppy
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_SHORTCODE=your_mpesa_shortcode
MPESA_PASSKEY=your_mpesa_passkey
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-domain.com/payments/callback/
```

## Deployment on Render

1. **Connect your GitHub repository to Render**

2. **Create a new Web Service**
   - Choose your repository
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn django_ecommerce.wsgi`

3. **Set Environment Variables in Render Dashboard**
   - Add all variables from `.env.example`
   - Set `DJANGO_DEBUG=False` for production
   - Update `MPESA_CALLBACK_URL` with your Render domain

4. **Deploy**
   - Render will automatically deploy on every push to main branch

## M-Pesa Integration

The platform includes comprehensive M-Pesa STK Push integration:

- **Payment Initiation** - Send STK push to customer's phone
- **Payment Verification** - Query M-Pesa API for payment status
- **Manual Confirmation** - Fallback for API failures
- **Payment Tracking** - Complete transaction history

### Testing M-Pesa

1. Use M-Pesa sandbox credentials
2. Test with phone numbers: `254708374149`, `254711111111`
3. Use Ngrok for local webhook testing
4. Check payment status in admin dashboard

## Project Structure

```
campus-shoppy/
├── django_ecommerce/     # Main Django project
├── shop/                 # Product catalog app
├── cart/                 # Shopping cart app
├── payments/             # M-Pesa payment app
├── account/              # User authentication
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── media/                # User uploads
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment
├── render.yaml          # Render deployment config
└── .env.example         # Environment template
```

## Security Features

- ✅ Environment-based secrets
- ✅ CSRF protection
- ✅ Secure cookies (production)
- ✅ HTTPS redirect (production)
- ✅ HSTS headers
- ✅ SQL injection protection
- ✅ XSS protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.


