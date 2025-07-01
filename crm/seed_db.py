from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import datetime, timedelta
import random

from crm.models import Customer, Product, Order


class Command(BaseCommand):
    help = 'Seed the database with sample CRM data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=10,
            help='Number of customers to create (default: 10)',
        )
        parser.add_argument(
            '--products',
            type=int,
            default=15,
            help='Number of products to create (default: 15)',
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=20,
            help='Number of orders to create (default: 20)',
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")
        
        # Check if migrations need to be applied
        from django.core.management import call_command
        try:
            call_command('migrate', verbosity=0)
            self.stdout.write("✓ Migrations applied")
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Migration warning: {str(e)}"))
        
        if options['clear']:
            self.clear_data()
        
        customers = self.create_customers(options['customers'])
        products = self.create_products(options['products'])
        orders = self.create_orders(customers, products, options['orders'])
        
        self.print_summary()

    def clear_data(self):
        """Clear existing data from the database."""
        self.stdout.write("Clearing existing data...")
        try:
            Order.objects.all().delete()
            Product.objects.all().delete()
            Customer.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Data cleared successfully!"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Warning: Could not clear data - {str(e)}"))
            self.stdout.write("This might be because tables don't exist yet. Continuing...")
            pass

    def create_customers(self, count):
        """Create sample customers."""
        self.stdout.write(f"Creating {count} customers...")
        
        customers_data = [
            {'name': 'Alice Johnson', 'email': 'alice.johnson@example.com', 'phone': '+1234567890'},
            {'name': 'Bob Smith', 'email': 'bob.smith@example.com', 'phone': '123-456-7890'},
            {'name': 'Carol Williams', 'email': 'carol.williams@example.com', 'phone': '+1987654321'},
            {'name': 'David Brown', 'email': 'david.brown@example.com', 'phone': '987-654-3210'},
            {'name': 'Eva Davis', 'email': 'eva.davis@example.com', 'phone': '+1122334455'},
            {'name': 'Frank Miller', 'email': 'frank.miller@example.com', 'phone': '555-123-4567'},
            {'name': 'Grace Wilson', 'email': 'grace.wilson@example.com', 'phone': '+1999888777'},
            {'name': 'Henry Taylor', 'email': 'henry.taylor@example.com', 'phone': '444-555-6666'},
            {'name': 'Ivy Anderson', 'email': 'ivy.anderson@example.com', 'phone': '+1777666555'},
            {'name': 'Jack Thomas', 'email': 'jack.thomas@example.com', 'phone': '333-222-1111'},
            {'name': 'Karen White', 'email': 'karen.white@example.com', 'phone': '+1555444333'},
            {'name': 'Liam Garcia', 'email': 'liam.garcia@example.com', 'phone': '666-777-8888'},
            {'name': 'Mia Rodriguez', 'email': 'mia.rodriguez@example.com', 'phone': '+1888999000'},
            {'name': 'Noah Martinez', 'email': 'noah.martinez@example.com', 'phone': '111-222-3333'},
            {'name': 'Olivia Hernandez', 'email': 'olivia.hernandez@example.com', 'phone': '+1444555666'},
        ]
        
        customers = []
        for i in range(min(count, len(customers_data))):
            customer = Customer.objects.create(**customers_data[i])
            customers.append(customer)
        
        # If we need more customers than predefined, generate them
        for i in range(len(customers_data), count):
            customer_data = {
                'name': f'Customer {i+1}',
                'email': f'customer{i+1}@example.com',
                'phone': f'+1{random.randint(1000000000, 9999999999)}'
            }
            customer = Customer.objects.create(**customer_data)
            customers.append(customer)
        
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(customers)} customers successfully!"))
        return customers

    def create_products(self, count):
        """Create sample products."""
        self.stdout.write(f"Creating {count} products...")
        
        products_data = [
            {'name': 'MacBook Pro 16"', 'price': Decimal('2499.99'), 'stock': 15},
            {'name': 'Dell XPS 13', 'price': Decimal('1299.99'), 'stock': 25},
            {'name': 'iPhone 15 Pro', 'price': Decimal('999.99'), 'stock': 50},
            {'name': 'Samsung Galaxy S24', 'price': Decimal('899.99'), 'stock': 40},
            {'name': 'iPad Air', 'price': Decimal('599.99'), 'stock': 30},
            {'name': 'AirPods Pro', 'price': Decimal('249.99'), 'stock': 100},
            {'name': 'Sony WH-1000XM5', 'price': Decimal('399.99'), 'stock': 20},
            {'name': 'Microsoft Surface Pro', 'price': Decimal('1199.99'), 'stock': 18},
            {'name': 'Apple Watch Series 9', 'price': Decimal('429.99'), 'stock': 35},
            {'name': 'Nintendo Switch OLED', 'price': Decimal('349.99'), 'stock': 45},
            {'name': 'LG 27" 4K Monitor', 'price': Decimal('449.99'), 'stock': 12},
            {'name': 'Logitech MX Master 3', 'price': Decimal('99.99'), 'stock': 60},
            {'name': 'Mechanical Keyboard', 'price': Decimal('159.99'), 'stock': 25},
            {'name': 'Webcam HD 1080p', 'price': Decimal('79.99'), 'stock': 40},
            {'name': 'Bluetooth Speaker', 'price': Decimal('129.99'), 'stock': 55},
            {'name': 'Gaming Mouse', 'price': Decimal('89.99'), 'stock': 70},
            {'name': 'USB-C Hub', 'price': Decimal('49.99'), 'stock': 80},
            {'name': 'Wireless Charger', 'price': Decimal('39.99'), 'stock': 90},
            {'name': 'External SSD 1TB', 'price': Decimal('149.99'), 'stock': 35},
            {'name': 'Phone Case', 'price': Decimal('24.99'), 'stock': 200},
        ]
        
        products = []
        for i in range(min(count, len(products_data))):
            product = Product.objects.create(**products_data[i])
            products.append(product)
        
        # If we need more products than predefined, generate them
        for i in range(len(products_data), count):
            product_data = {
                'name': f'Product {i+1}',
                'price': Decimal(f'{random.uniform(10, 1000):.2f}'),
                'stock': random.randint(5, 100)
            }
            product = Product.objects.create(**product_data)
            products.append(product)
        
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(products)} products successfully!"))
        return products

    def create_orders(self, customers, products, count):
        """Create sample orders."""
        self.stdout.write(f"Creating {count} orders...")
        
        orders = []
        
        with transaction.atomic():
            for i in range(count):
                # Select random customer
                customer = random.choice(customers)
                
                # Select 1-4 random products for each order
                num_products = random.randint(1, min(4, len(products)))
                selected_products = random.sample(products, num_products)
                
                # Create order
                order = Order.objects.create(customer=customer)
                order.products.set(selected_products)
                
                # Calculate total amount
                total = sum(product.price for product in selected_products)
                order.total_amount = total
                order.save(update_fields=['total_amount'])
                
                # Update order date to a random date in the last 30 days
                days_ago = random.randint(0, 30)
                order_date = datetime.now() - timedelta(days=days_ago)
                Order.objects.filter(id=order.id).update(
                    order_date=order_date,
                    created_at=order_date
                )
                
                orders.append(order)
        
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(orders)} orders successfully!"))
        return orders

    def print_summary(self):
        """Print a summary of created data."""
        self.stdout.write("\n" + "="*60)
        self.stdout.write("DATABASE SEEDING COMPLETED!")
        self.stdout.write("="*60)
        
        customer_count = Customer.objects.count()
        product_count = Product.objects.count()
        order_count = Order.objects.count()
        
        self.stdout.write(f"Total Customers: {customer_count}")
        self.stdout.write(f"Total Products: {product_count}")
        self.stdout.write(f"Total Orders: {order_count}")
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write("You can now test your GraphQL mutations and queries!")
        self.stdout.write("Visit http://localhost:8000/graphql/ to start testing.")
        self.stdout.write("="*60)
