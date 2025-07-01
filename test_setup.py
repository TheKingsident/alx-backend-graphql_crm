#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

try:
    from crm.models import Customer, Product, Order
    print("✓ Models imported successfully")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    print("✓ Database connection successful")
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'crm_%';")
    tables = cursor.fetchall()
    print(f"✓ Found tables: {[table[0] for table in tables]}")
    
    # Count existing records
    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    
    print(f"✓ Current data counts:")
    print(f"  - Customers: {customer_count}")
    print(f"  - Products: {product_count}")
    print(f"  - Orders: {order_count}")
    
    # Try creating a test customer
    if customer_count == 0:
        test_customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="+1234567890"
        )
        print(f"✓ Created test customer: {test_customer}")
    
    print("✓ Everything looks good! You can now run the seed command.")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
