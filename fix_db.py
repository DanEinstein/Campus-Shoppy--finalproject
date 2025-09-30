#!/usr/bin/env python
"""
Database fix script for Render deployment
This script ensures the database schema is correct
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ecommerce.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def fix_database():
    """Fix database schema issues"""
    print("Fixing database schema...")
    
    with connection.cursor() as cursor:
        # Check if cart_order table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cart_order'")
        if not cursor.fetchone():
            print("Creating cart_order table...")
            call_command('migrate', 'cart', verbosity=0)
            return
        
        # Check if updated column exists
        cursor.execute("PRAGMA table_info(cart_order)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'updated' not in columns:
            print("Adding missing 'updated' column...")
            try:
                cursor.execute("ALTER TABLE cart_order ADD COLUMN updated DATETIME DEFAULT CURRENT_TIMESTAMP")
                print("Successfully added 'updated' column")
            except Exception as e:
                print(f"Error adding column: {e}")
        else:
            print("'updated' column already exists")
    
    # Check shop_product table for featured column
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shop_product'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(shop_product)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'featured' not in columns:
                print("Adding missing 'featured' column to shop_product...")
                try:
                    cursor.execute("ALTER TABLE shop_product ADD COLUMN featured BOOLEAN DEFAULT 0")
                    print("Successfully added 'featured' column")
                except Exception as e:
                    print(f"Error adding featured column: {e}")
            else:
                print("'featured' column already exists in shop_product")
    
    # Run all migrations to ensure everything is up to date
    print("Running migrations...")
    call_command('migrate', verbosity=0)
    print("Database fix completed!")

if __name__ == '__main__':
    fix_database()
