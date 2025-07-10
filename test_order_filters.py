"""
Test script for OrderFilter functionality.

This script tests all the OrderFilter features including related field lookups,
many-to-many filtering, and the challenge feature for filtering by product ID.
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append('/home/cakemurderer/ALX_Projects/alx_backend_graphql')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Customer, Product, Order
from crm.filters import OrderFilter, AdvancedOrderFilter
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta


def create_test_data():
    """Create comprehensive test data for order filtering."""
    print("Creating test data for OrderFilter...")
    
    # Create customers
    customers_data = [
        {'name': 'John Doe', 'email': 'john.doe@gmail.com', 'phone': '+1234567890'},
        {'name': 'Jane Smith', 'email': 'jane.smith@yahoo.com', 'phone': '+1987654321'},
        {'name': 'Bob Johnson', 'email': 'bob.johnson@gmail.com', 'phone': '+44123456789'},
        {'name': 'Alice Brown', 'email': 'alice.brown@company.com', 'phone': '+1555123456'},
    ]
    
    customers = []
    for customer_data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=customer_data['email'],
            defaults=customer_data
        )
        customers.append(customer)
        if created:
            print(f"Created customer: {customer.name}")
    
    # Create products
    products_data = [
        {'name': 'Gaming Laptop', 'price': Decimal('1299.99'), 'stock': 10},
        {'name': 'Office Laptop', 'price': Decimal('699.99'), 'stock': 15},
        {'name': 'Premium Smartphone', 'price': Decimal('899.99'), 'stock': 20},
        {'name': 'Wireless Headphones', 'price': Decimal('199.99'), 'stock': 30},
        {'name': 'Professional Monitor', 'price': Decimal('399.99'), 'stock': 12},
        {'name': 'Mechanical Keyboard', 'price': Decimal('149.99'), 'stock': 25},
    ]
    
    products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        products.append(product)
        if created:
            print(f"Created product: {product.name}")
    
    # Create orders with different scenarios
    orders_data = [
        {
            'customer': customers[0],  # John Doe
            'products': [products[0], products[3]],  # Gaming Laptop + Headphones
            'total_amount': Decimal('1499.98'),
            'days_ago': 5
        },
        {
            'customer': customers[1],  # Jane Smith
            'products': [products[1]],  # Office Laptop
            'total_amount': Decimal('699.99'),
            'days_ago': 15
        },
        {
            'customer': customers[0],  # John Doe (repeat customer)
            'products': [products[2], products[4]],  # Smartphone + Monitor
            'total_amount': Decimal('1299.98'),
            'days_ago': 25
        },
        {
            'customer': customers[2],  # Bob Johnson
            'products': [products[3], products[5]],  # Headphones + Keyboard
            'total_amount': Decimal('349.98'),
            'days_ago': 10
        },
        {
            'customer': customers[3],  # Alice Brown
            'products': [products[0], products[2], products[4]],  # Laptop + Phone + Monitor
            'total_amount': Decimal('2599.97'),
            'days_ago': 3
        },
        {
            'customer': customers[1],  # Jane Smith (repeat customer)
            'products': [products[5]],  # Keyboard only
            'total_amount': Decimal('149.99'),
            'days_ago': 35
        }
    ]
    
    orders = []
    for order_data in orders_data:
        # Calculate order date
        order_date = timezone.now() - timedelta(days=order_data['days_ago'])
        
        order, created = Order.objects.get_or_create(
            customer=order_data['customer'],
            total_amount=order_data['total_amount'],
            order_date=order_date,
            defaults={'created_at': order_date}
        )
        
        if created:
            # Add products to the order
            order.products.set(order_data['products'])
            orders.append(order)
            print(f"Created order: {order.customer.name} - ${order.total_amount} ({len(order_data['products'])} products)")
    
    print(f"\nTest data summary:")
    print(f"Customers: {Customer.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    
    return customers, products, orders


def test_total_amount_filters():
    """Test total amount range filtering."""
    print("\n=== Testing Total Amount Filters ===")
    
    # Test orders with total amount >= $500
    filter_data = {'total_amount_gte': 500}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"Orders with total amount >= $500:")
    for order in results:
        print(f"  - {order.customer.name}: ${order.total_amount} (Order Date: {order.order_date.strftime('%Y-%m-%d')})")
    
    # Test orders between $200 and $1000
    filter_data = {'total_amount_gte': 200, 'total_amount_lte': 1000}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"\nOrders between $200 and $1000:")
    for order in results:
        print(f"  - {order.customer.name}: ${order.total_amount}")


def test_date_filters():
    """Test order date range filtering."""
    print("\n=== Testing Date Range Filters ===")
    
    # Test orders from last 20 days
    twenty_days_ago = timezone.now() - timedelta(days=20)
    filter_data = {'order_date_gte': twenty_days_ago}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"Orders from the last 20 days:")
    for order in results:
        days_ago = (timezone.now() - order.order_date).days
        print(f"  - {order.customer.name}: ${order.total_amount} ({days_ago} days ago)")


def test_customer_name_filter():
    """Test filtering by customer name (related field lookup)."""
    print("\n=== Testing Customer Name Filter (Related Field) ===")
    
    # Test filtering by customer name containing "john"
    filter_data = {'customer_name': 'john'}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"Orders from customers with 'john' in their name:")
    for order in results:
        print(f"  - Customer: {order.customer.name} (${order.total_amount})")
        print(f"    Products: {', '.join([p.name for p in order.products.all()])}")
    
    # Test filtering by customer email domain
    filter_data = {'customer_email': 'gmail'}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"\nOrders from customers with Gmail addresses:")
    for order in results:
        print(f"  - {order.customer.name} ({order.customer.email}): ${order.total_amount}")


def test_product_name_filter():
    """Test filtering by product name (many-to-many related field)."""
    print("\n=== Testing Product Name Filter (Many-to-Many) ===")
    
    # Test filtering orders containing products with "laptop" in the name
    filter_data = {'product_name': 'laptop'}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"Orders containing products with 'laptop' in the name:")
    for order in results:
        print(f"  - {order.customer.name}: ${order.total_amount}")
        laptop_products = [p.name for p in order.products.all() if 'laptop' in p.name.lower()]
        print(f"    Laptop products: {', '.join(laptop_products)}")
        print(f"    All products: {', '.join([p.name for p in order.products.all()])}")


def test_product_id_filter():
    """Test the CHALLENGE filter - filtering by specific product ID."""
    print("\n=== Testing Product ID Filter (CHALLENGE) ===")
    
    # Get a specific product to test with
    gaming_laptop = Product.objects.filter(name__icontains='gaming laptop').first()
    
    if gaming_laptop:
        print(f"Testing with Gaming Laptop ID: {gaming_laptop.id}")
        
        # Test filtering orders containing the specific product ID
        filter_data = {'product_id': str(gaming_laptop.id)}
        order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
        results = order_filter.qs
        
        print(f"Orders containing Gaming Laptop (ID: {gaming_laptop.id}):")
        for order in results:
            print(f"  - {order.customer.name}: ${order.total_amount}")
            print(f"    Products: {', '.join([p.name for p in order.products.all()])}")
            print(f"    Contains Gaming Laptop: {'Yes' if gaming_laptop in order.products.all() else 'No'}")
    
    # Test the flexible contains_product filter
    filter_data = {'contains_product': 'Gaming Laptop'}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"\nUsing flexible contains_product filter with 'Gaming Laptop':")
    for order in results:
        print(f"  - {order.customer.name}: ${order.total_amount}")
        print(f"    Products: {', '.join([p.name for p in order.products.all()])}")


def test_custom_filters():
    """Test custom filter methods."""
    print("\n=== Testing Custom Filters ===")
    
    # Test high value orders filter
    filter_data = {'high_value_orders': True}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"High-value orders (> $500):")
    for order in results:
        print(f"  - {order.customer.name}: ${order.total_amount}")
    
    # Test recent orders filter
    filter_data = {'recent_orders': True}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"\nRecent orders (last 30 days):")
    for order in results:
        days_ago = (timezone.now() - order.order_date).days
        print(f"  - {order.customer.name}: ${order.total_amount} ({days_ago} days ago)")
    
    # Test minimum products filter
    filter_data = {'min_products': 2}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"\nOrders with at least 2 products:")
    for order in results:
        product_count = order.products.count()
        print(f"  - {order.customer.name}: {product_count} products (${order.total_amount})")
        print(f"    Products: {', '.join([p.name for p in order.products.all()])}")


def test_order_value_categories():
    """Test order value category filter."""
    print("\n=== Testing Order Value Categories ===")
    
    categories = ['small', 'medium', 'large', 'enterprise']
    
    for category in categories:
        filter_data = {'order_value_category': category}
        order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
        results = order_filter.qs
        
        print(f"\n{category.title()} orders:")
        for order in results:
            print(f"  - {order.customer.name}: ${order.total_amount}")


def test_combined_filters():
    """Test combining multiple filters."""
    print("\n=== Testing Combined Filters ===")
    
    # High-value recent orders from Gmail customers
    filter_data = {
        'customer_email': 'gmail',
        'high_value_orders': True,
        'recent_orders': True
    }
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"High-value recent orders from Gmail customers:")
    for order in results:
        days_ago = (timezone.now() - order.order_date).days
        print(f"  - {order.customer.name} ({order.customer.email})")
        print(f"    Amount: ${order.total_amount} ({days_ago} days ago)")
        print(f"    Products: {', '.join([p.name for p in order.products.all()])}")
    
    # Orders containing laptops from customers named John
    filter_data = {
        'customer_name': 'john',
        'product_name': 'laptop'
    }
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    results = order_filter.qs
    
    print(f"\nLaptop orders from customers named John:")
    for order in results:
        print(f"  - {order.customer.name}: ${order.total_amount}")
        print(f"    Products: {', '.join([p.name for p in order.products.all()])}")


def test_advanced_search():
    """Test the advanced search filter."""
    print("\n=== Testing Advanced Search Filter ===")
    
    # Test search across multiple fields
    filter_data = {'search': 'john'}
    advanced_filter = AdvancedOrderFilter(filter_data, queryset=Order.objects.all())
    results = advanced_filter.qs
    
    print(f"Search results for 'john' (across customer name, email, and product names):")
    for order in results:
        print(f"  - Customer: {order.customer.name} ({order.customer.email})")
        print(f"    Amount: ${order.total_amount}")
        print(f"    Products: {', '.join([p.name for p in order.products.all()])}")


def generate_sales_report():
    """Generate a comprehensive sales report using filters."""
    print("\n=== SALES REPORT ===")
    
    # Recent high-value orders
    filter_data = {'recent_orders': True, 'high_value_orders': True}
    order_filter = OrderFilter(filter_data, queryset=Order.objects.all())
    recent_high_value = order_filter.qs
    
    print(f"📈 RECENT HIGH-VALUE ORDERS ({recent_high_value.count()} orders):")
    total_recent_high_value = sum(order.total_amount for order in recent_high_value)
    for order in recent_high_value:
        days_ago = (timezone.now() - order.order_date).days
        print(f"  - {order.customer.name}: ${order.total_amount} ({days_ago} days ago)")
    print(f"  Total Value: ${total_recent_high_value}")
    
    # Orders by customer segment
    gmail_filter = OrderFilter({'customer_email': 'gmail'}, queryset=Order.objects.all())
    gmail_orders = gmail_filter.qs
    
    print(f"\n👥 CUSTOMER SEGMENTS:")
    print(f"  Gmail customers: {gmail_orders.count()} orders")
    print(f"  Gmail total value: ${sum(order.total_amount for order in gmail_orders)}")
    
    # Product performance
    laptop_filter = OrderFilter({'product_name': 'laptop'}, queryset=Order.objects.all())
    laptop_orders = laptop_filter.qs
    
    print(f"\n💻 PRODUCT PERFORMANCE:")
    print(f"  Laptop orders: {laptop_orders.count()} orders")
    print(f"  Laptop revenue: ${sum(order.total_amount for order in laptop_orders)}")
    
    # Order size analysis
    large_orders = OrderFilter({'min_products': 3}, queryset=Order.objects.all()).qs
    print(f"\n📦 ORDER SIZE ANALYSIS:")
    print(f"  Large orders (3+ products): {large_orders.count()}")
    print(f"  Average products per large order: {sum(order.products.count() for order in large_orders) / max(large_orders.count(), 1):.1f}")


def run_all_tests():
    """Run all OrderFilter tests."""
    print("Starting OrderFilter Tests")
    print("=" * 70)
    
    # Create test data
    customers, products, orders = create_test_data()
    
    # Run individual tests
    test_total_amount_filters()
    test_date_filters()
    test_customer_name_filter()
    test_product_name_filter()
    test_product_id_filter()
    test_custom_filters()
    test_order_value_categories()
    test_combined_filters()
    test_advanced_search()
    
    # Generate comprehensive report
    generate_sales_report()
    
    print("\n" + "=" * 70)
    print("All OrderFilter tests completed!")
    print("\n💡 Key Learning Points:")
    print("  ✅ Related field lookups use double underscore (__)")
    print("  ✅ Many-to-many filtering works with products__field")
    print("  ✅ Custom filters enable complex business logic")
    print("  ✅ UUID filtering works for challenge requirements")
    print("  ✅ Combining filters creates powerful query capabilities")
    print("  ✅ .distinct() may be needed for many-to-many queries")


if __name__ == "__main__":
    run_all_tests()
