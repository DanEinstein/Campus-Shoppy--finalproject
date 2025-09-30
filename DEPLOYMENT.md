# Deployment Checklist

## Pre-Deployment Checklist

### ✅ Code Preparation
- [x] All dependencies in `requirements.txt`
- [x] Environment variables externalized
- [x] `.env` file in `.gitignore`
- [x] Static files configuration (WhiteNoise)
- [x] Database migrations ready
- [x] Security settings configured

### ✅ Files Created
- [x] `requirements.txt` - All dependencies with versions
- [x] `Procfile` - Heroku deployment
- [x] `render.yaml` - Render deployment configuration
- [x] `.env.example` - Environment template
- [x] `.gitignore` - Comprehensive ignore rules
- [x] `README.md` - Complete documentation

## GitHub Setup

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Campus Shoppy e-commerce platform"
```

### 2. Create GitHub Repository
1. Go to GitHub.com
2. Click "New repository"
3. Name: `campus-shoppy`
4. Description: "Django e-commerce platform with M-Pesa integration"
5. Make it public or private
6. Don't initialize with README (we already have one)

### 3. Push to GitHub
```bash
git remote add origin https://github.com/yourusername/campus-shoppy.git
git branch -M main
git push -u origin main
```

## Render Deployment

### 1. Connect Repository
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub account
5. Select `campus-shoppy` repository

### 2. Configure Service
- **Name**: `campus-shoppy`
- **Environment**: `Python 3.11.10`
- **Region**: Choose closest to Kenya
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `gunicorn django_ecommerce.wsgi`

### 3. Set Environment Variables
In Render dashboard, go to Environment tab and add:

```
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*.onrender.com,campus-shoppy-maseno-7y1e.onrender.com
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_SHORTCODE=your_mpesa_shortcode
MPESA_PASSKEY=your_mpesa_passkey
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://campus-shoppy-maseno-7y1e.onrender.com/payments/callback/
```

### 4. Deploy
1. Click "Create Web Service"
2. Render will build and deploy automatically
3. Wait for deployment to complete
4. Test your live site!

## Post-Deployment Testing

### ✅ Basic Functionality
- [ ] Homepage loads
- [ ] Product catalog displays
- [ ] User registration/login works
- [ ] Cart functionality works
- [ ] M-Pesa payment initiation works
- [ ] Payment verification works

### ✅ M-Pesa Testing
1. **Test Payment Flow**:
   - Add items to cart
   - Proceed to checkout
   - Enter phone number
   - Check if STK push is sent

2. **Test Payment Verification**:
   - Use "Verify Payment" button
   - Test manual confirmation
   - Check payment status updates

3. **Test Callbacks**:
   - Use Ngrok for local testing
   - Update `MPESA_CALLBACK_URL` in Render
   - Test webhook reception

## Monitoring & Maintenance

### ✅ Regular Checks
- [ ] Monitor Render logs for errors
- [ ] Check M-Pesa API status
- [ ] Verify payment callbacks are working
- [ ] Update dependencies regularly
- [ ] Backup database (if using external DB)

### ✅ Security
- [ ] Keep Django and dependencies updated
- [ ] Monitor for security vulnerabilities
- [ ] Use strong secret keys
- [ ] Enable HTTPS (Render provides this automatically)

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check `requirements.txt` for missing packages
   - Verify Python version compatibility
   - Check build logs in Render dashboard

2. **M-Pesa Issues**:
   - Verify API credentials
   - Check callback URL is accessible
   - Test with sandbox credentials first

3. **Static Files**:
   - Ensure `collectstatic` runs during build
   - Check WhiteNoise configuration
   - Verify static file paths

4. **Database Issues**:
   - Run migrations during build
   - Check database connection settings
   - Verify database permissions

## Support

For issues with:
- **Django**: Check Django documentation
- **Render**: Check Render documentation
- **M-Pesa**: Check Safaricom Daraja API docs
- **This Project**: Create GitHub issue
