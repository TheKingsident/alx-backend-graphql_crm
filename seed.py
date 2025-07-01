#!/usr/bin/env python
"""
Seed script for the CRM system.
This script populates the database with sample customers, products, and orders.

Usage:
    python seed.py
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Customer, Product, Order


def clear_data():
    """Clear existing data from the database."""
    print("Clearing existing data...")
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    print("✓ Data cleared successfully!")


def create_customers():
    """Create sample customers."""
    print("Creating customers...")
    
    customers_data = [
        {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@example.com',
            'phone': '+1234567890'
        },
        {
            'name': 'Bob Smith',
            'email': 'bob.smith@example.com',
            'phone': '123-456-7890'
        },
        {
            'name': 'Carol Williams',
            'email': 'carol.williams@example.com',
            'phone': '+1987654321'
        },
        {
            'name': 'David Brown',
            'email': 'david.brown@example.com',
            'phone': '987-654-3210'
        },
        {
            'name': 'Eva Davis',
            'email': 'eva.davis@example.com',
            'phone': '+1122334455'
        },
        {
            'name': 'Frank Miller',
            'email': 'frank.miller@example.com',
            'phone': '555-123-4567'
        },
        {
            'name': 'Grace Wilson',
            'email': 'grace.wilson@example.com',
            'phone': '+1999888777'
        },
        {
            'name': 'Henry Taylor',
            'email': 'henry.taylor@example.com',
            'phone': '444-555-6666'
        },
        {
            'name': 'Ivy Anderson',
            'email': 'ivy.anderson@example.com',
            'phone': '+1777666555'
        },
        {
            'name': 'Jack Thomas',
            'email': 'jack.thomas@example.com',
            'phone': '333-222-1111'
        }
    ]
    
    customers = []
    for customer_data in customers_data:
        customer = Customer.objects.create(**customer_data)
        customers.append(customer)
        print(f"  ✓ Created customer: {customer.name}")
    
    print(f"✓ Created {len(customers)} customers successfully!")
    return customers


def create_products():
    """Create sample products."""
    print("Creating products...")
    
    products_data = [
        {
            'name': 'MacBook Pro 16"',
            'price': Decimal('2499.99'),
            'stock': 15
        },
        {
            'name': 'Dell XPS 13',
            'price': Decimal('1299.99'),
            'stock': 25
        },
        {
            'name': 'iPhone 15 Pro',
            'price': Decimal('999.99'),
            'stock': 50
        },
        {
            'name': 'Samsung Galaxy S24',
            'price': Decimal('899.99'),
            'stock': 40
        },
        {
            'name': 'iPad Air',
            'price': Decimal('599.99'),
            'stock': 30
        },
        {
            'name': 'AirPods Pro',
            'price': Decimal('249.99'),
            'stock': 100
        },
        {
            'name': 'Sony WH-1000XM5',
            'price': Decimal('399.99'),
            'stock': 20
        },
        {
            'name': 'Microsoft Surface Pro',
            'price': Decimal('1199.99'),
            'stock': 18
        },
        {
            'name': 'Apple Watch Series 9',
            'price': Decimal('429.99'),
            'stock': 35
        },
        {
            'name': 'Nintendo Switch OLED',
            'price': Decimal('349.99'),
            'stock': 45
        },
        {
            'name': 'LG 27" 4K Monitor',
            'price': Decimal('449.99'),
            'stock': 12
        },
        {
            'name': 'Logitech MX Master 3',
            'price': Decimal('99.99'),
            'stock': 60
        },
        {
            'name': 'Mechanical Keyboard',
            'price': Decimal('159.99'),
            'stock': 25
        },
        {
            'name': 'Webcam HD 1080p',
            'price': Decimal('79.99'),
            'stock': 40
        },
        {
            'name': 'Bluetooth Speaker',
            'price': Decimal('129.99'),
            'stock': 55
        }
    ]
    
    products = []
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        products.append(product)
        print(f"  ✓ Created product: {product.name} - ${product.price}")
    
    print(f"✓ Created {len(products)} products successfully!")
    return products


def create_orders(customers, products):
    """Create sample orders."""
    print("Creating orders...")
    
    orders = []
    
    # Create 20 random orders
    for i in range(20):
        # Select random customer
        customer = random.choice(customers)
        
        # Select 1-4 random products for each order
        num_products = random.randint(1, 4)
        selected_products = random.sample(products, num_products)
        
        # Create order with random date in the last 30 days
        days_ago = random.randint(0, 30)
        order_date = datetime.now() - timedelta(days=days_ago)
        
        # Create the order
        order = Order.objects.create(customer=customer)
        order.products.set(selected_products)
        
        # Calculate total amount
        total = sum(product.price for product in selected_products)
        order.total_amount = total
        order.save(update_fields=['total_amount'])
        
        # Update the created_at and order_date to the random date
        Order.objects.filter(id=order.id).update(
            order_date=order_date,
            created_at=order_date
        )
        
        orders.append(order)
        product_names = [p.name for p in selected_products]
        print(f"  ✓ Created order for {customer.name}: {', '.join(product_names)} - ${total}")
    
    print(f"✓ Created {len(orders)} orders successfully!")
    return orders


def print_summary():
    """Print a summary of created data."""
    print("\n" + "="*60)
    print("DATABASE SEEDING COMPLETED!")
    print("="*60)
    
    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    
    print(f"Total Customers: {customer_count}")
    print(f"Total Products: {product_count}")
    print(f"Total Orders: {order_count}")
    
    # Show some sample data
    print("\nSample Customers:")
    for customer in Customer.objects.all()[:5]:
        print(f"  - {customer.name} ({customer.email})")
    
    print("\nSample Products:")
    for product in Product.objects.all()[:5]:
        print(f"  - {product.name}: ${product.price} (Stock: {product.stock})")
    
    print("\nSample Orders:")
    for order in Order.objects.all()[:5]:
        product_count = order.products.count()
        print(f"  - Order #{str(order.id)[:8]}... for {order.customer.name}: {product_count} products, Total: ${order.total_amount}")
    
    print("\n" + "="*60)
    print("You can now test your GraphQL mutations and queries!")
    print("Visit http://localhost:8000/graphql/ to start testing.")
    print("="*60)


def main():
    """Main function to run the seeding process."""
    print("Starting database seeding...")
    print("="*60)
    
    try:
        # Clear existing data
        clear_data()
        
        # Create new data
        customers = create_customers()
        products = create_products()
        orders = create_orders(customers, products)
        
        # Print summary
        print_summary()
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
