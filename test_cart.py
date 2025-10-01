#!/usr/bin/env python
"""
Test script to verify cart functionality
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ecommerce.settings')
django.setup()

from cart.cart import Cart
from shop.models import Product
from django.test import RequestFactory
from django.contrib.auth.models import User

def test_cart_serialization():
    """Test that cart can be serialized without Decimal errors"""
    print("Testing cart serialization...")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/cart/')
    request.session = {}
    
    # Create cart instance
    cart = Cart(request)
    
    # Get a product (or create one for testing)
    try:
        product = Product.objects.first()
        if not product:
            print("No products found. Creating a test product...")
            product = Product.objects.create(
                name="Test Product",
                price=100.00,
                description="Test product for cart testing",
                inventory=10
            )
    except Exception as e:
        print(f"Error getting product: {e}")
        return False
    
    # Add product to cart
    cart.add(product, quantity=2)
    
    # Test cart iteration (this is where the error occurred)
    try:
        items = list(cart)
        print(f"Cart items: {len(items)}")
        for item in items:
            print(f"Item: {item['product'].name}, Price: {item['price']}, Total: {item['total_price']}")
        
        # Test total price calculation
        total = cart.get_total_price()
        print(f"Total price: {total}")
        
        # Test session serialization
        cart.save()
        print("Cart saved to session successfully")
        
        return True
        
    except Exception as e:
        print(f"Error in cart operations: {e}")
        return False

def test_cart_json_serialization():
    """Test that cart data can be JSON serialized"""
    print("\nTesting cart JSON serialization...")
    
    import json
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/cart/')
    request.session = {}
    
    # Create cart instance
    cart = Cart(request)
    
    # Get a product
    try:
        product = Product.objects.first()
        if not product:
            print("No products found for JSON test")
            return False
    except Exception as e:
        print(f"Error getting product for JSON test: {e}")
        return False
    
    # Add product to cart
    cart.add(product, quantity=1)
    
    # Test JSON serialization of cart data
    try:
        cart_data = dict(cart.cart)
        json_str = json.dumps(cart_data)
        print("Cart data JSON serialized successfully")
        print(f"JSON data: {json_str}")
        return True
    except Exception as e:
        print(f"Error serializing cart to JSON: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Cart Functionality Test")
    print("=" * 50)
    
    # Test 1: Basic cart serialization
    test1_passed = test_cart_serialization()
    
    # Test 2: JSON serialization
    test2_passed = test_cart_json_serialization()
    
    print("\n" + "=" * 50)
    print("📊 Test Results")
    print("=" * 50)
    print(f"✅ Cart Serialization: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ JSON Serialization: {'PASSED' if test2_passed else 'FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Cart is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    print("=" * 50)
