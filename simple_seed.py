#!/usr/bin/env python3
"""
Simple seeding script for CRM data
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

# Now import models
from crm.models import Customer, Product, Order

def main():
    print("Starting seeding process...")
    
    # Clear existing data
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    print("Cleared existing data")
    
    # Create customers
    customers = [
        Customer.objects.create(name="Alice Johnson", email="alice@example.com", phone="+1234567890"),
        Customer.objects.create(name="Bob Smith", email="bob@example.com", phone="123-456-7890"),
        Customer.objects.create(name="Carol Williams", email="carol@example.com", phone="+1987654321"),
    ]
    print(f"Created {len(customers)} customers")
    
    # Create products
    products = [
        Product.objects.create(name="MacBook Pro", price=Decimal('2499.99'), stock=10),
        Product.objects.create(name="iPhone 15", price=Decimal('999.99'), stock=25),
        Product.objects.create(name="iPad Air", price=Decimal('599.99'), stock=15),
        Product.objects.create(name="AirPods Pro", price=Decimal('249.99'), stock=50),
    ]
    print(f"Created {len(products)} products")
    
    # Create orders
    orders = []
    for i, customer in enumerate(customers):
        order = Order.objects.create(customer=customer)
        # Add some products to each order
        order.products.set(products[:2])  # Add first 2 products to each order
        # Calculate total
        total = sum(p.price for p in order.products.all())
        order.total_amount = total
        order.save()
        orders.append(order)
    
    print(f"Created {len(orders)} orders")
    print("Seeding completed successfully!")
    print(f"Total: {Customer.objects.count()} customers, {Product.objects.count()} products, {Order.objects.count()} orders")

if __name__ == '__main__':
    main()
