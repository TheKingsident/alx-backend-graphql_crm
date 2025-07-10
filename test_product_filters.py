"""
Test script for ProductFilter functionality.

This script tests all the ProductFilter features and demonstrates
how the filtering works with actual data.
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append('/home/cakemurderer/ALX_Projects/alx_backend_graphql')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Product
from crm.filters import ProductFilter, AdvancedProductFilter
from decimal import Decimal


def create_test_products():
    """Create test products for filter testing."""
    print("Creating test products...")
    
    test_products = [
        {
            'name': 'Gaming Laptop',
            'price': Decimal('1299.99'),
            'stock': 5
        },
        {
            'name': 'Office Laptop', 
            'price': Decimal('699.99'),
            'stock': 0  # Out of stock
        },
        {
            'name': 'Budget Tablet',
            'price': Decimal('199.99'),
            'stock': 25
        },
        {
            'name': 'Premium Smartphone',
            'price': Decimal('899.99'),
            'stock': 3  # Low stock
        },
        {
            'name': 'Wireless Headphones',
            'price': Decimal('49.99'),
            'stock': 50
        },
        {
            'name': 'Professional Monitor',
            'price': Decimal('399.99'),
            'stock': 8  # Low stock
        },
        {
            'name': 'Luxury Watch',
            'price': Decimal('2499.99'),
            'stock': 2  # Very low stock
        },
        {
            'name': 'Basic Mouse',
            'price': Decimal('19.99'),
            'stock': 100
        }
    ]
    
    for product_data in test_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"Created: {product.name} - ${product.price} (Stock: {product.stock})")
        else:
            print(f"Already exists: {product.name}")
    
    print(f"Total products in database: {Product.objects.count()}")


def test_name_filter():
    """Test the name filter with case-insensitive partial matching."""
    print("\n=== Testing Name Filter ===")
    
    # Test case-insensitive partial match
    filter_data = {'name': 'laptop'}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"Searching for products containing 'laptop':")
    for product in results:
        print(f"  - {product.name} (${product.price}) - Stock: {product.stock}")


def test_price_filters():
    """Test price filtering."""
    print("\n=== Testing Price Filters ===")
    
    # Test price greater than or equal to $200
    filter_data = {'price_gte': 200}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"Products with price >= $200:")
    for product in results:
        print(f"  - {product.name}: ${product.price}")
    
    # Test price less than or equal to $100
    filter_data = {'price_lte': 100}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nProducts with price <= $100:")
    for product in results:
        print(f"  - {product.name}: ${product.price}")
    
    # Test price range
    filter_data = {'price_gte': 100, 'price_lte': 500}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nProducts with price between $100 and $500:")
    for product in results:
        print(f"  - {product.name}: ${product.price}")


def test_stock_filters():
    """Test stock filtering."""
    print("\n=== Testing Stock Filters ===")
    
    # Test exact stock
    filter_data = {'stock': 0}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"Products with exactly 0 stock:")
    for product in results:
        print(f"  - {product.name} (Stock: {product.stock})")
    
    # Test stock greater than or equal to 10
    filter_data = {'stock_gte': 10}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nProducts with stock >= 10:")
    for product in results:
        print(f"  - {product.name} (Stock: {product.stock})")
    
    # Test stock less than or equal to 5
    filter_data = {'stock_lte': 5}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nProducts with stock <= 5:")
    for product in results:
        print(f"  - {product.name} (Stock: {product.stock})")


def test_low_stock_filter():
    """Test the custom low stock filter."""
    print("\n=== Testing Low Stock Filter (Challenge Answer!) ===")
    
    # Test low stock with threshold 10
    filter_data = {'low_stock': 10}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"Products with stock < 10 (Low Stock Alert!):")
    for product in results:
        print(f"  - {product.name}: {product.stock} units (${product.price})")
        if product.stock == 0:
            print(f"    ⚠️  OUT OF STOCK!")
        elif product.stock <= 3:
            print(f"    ⚠️  CRITICALLY LOW!")
        else:
            print(f"    ⚠️  Low stock - reorder soon")
    
    # Test with different threshold
    filter_data = {'low_stock': 5}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nProducts with stock < 5 (Critical Stock Level):")
    for product in results:
        print(f"  - {product.name}: {product.stock} units")


def test_stock_availability_filters():
    """Test out of stock and in stock filters."""
    print("\n=== Testing Stock Availability Filters ===")
    
    # Test out of stock
    filter_data = {'out_of_stock': True}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"Products that are OUT OF STOCK:")
    for product in results:
        print(f"  - {product.name} (${product.price}) - Stock: {product.stock}")
    
    # Test in stock
    filter_data = {'in_stock': True}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nProducts that are IN STOCK:")
    for product in results:
        print(f"  - {product.name} - Stock: {product.stock}")


def test_price_category_filter():
    """Test the price category filter."""
    print("\n=== Testing Price Category Filter ===")
    
    categories = ['budget', 'mid-range', 'premium', 'luxury']
    
    for category in categories:
        filter_data = {'price_category': category}
        product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
        results = product_filter.qs
        
        print(f"\n{category.title()} products:")
        for product in results:
            print(f"  - {product.name}: ${product.price}")


def test_combined_filters():
    """Test combining multiple filters."""
    print("\n=== Testing Combined Filters ===")
    
    # Low stock + budget category
    filter_data = {
        'low_stock': 10,
        'price_category': 'budget'
    }
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"Budget products with low stock (< 10 units):")
    for product in results:
        print(f"  - {product.name}: ${product.price} (Stock: {product.stock})")
    
    # In stock laptops under $1000
    filter_data = {
        'name': 'laptop',
        'in_stock': True,
        'price_lte': 1000
    }
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    results = product_filter.qs
    
    print(f"\nIn-stock laptops under $1000:")
    for product in results:
        print(f"  - {product.name}: ${product.price} (Stock: {product.stock})")


def test_advanced_filter_with_ordering():
    """Test the advanced filter with ordering."""
    print("\n=== Testing Advanced Filter with Ordering ===")
    
    # Order by price (ascending)
    filter_data = {'ordering': 'price'}
    advanced_filter = AdvancedProductFilter(filter_data, queryset=Product.objects.all())
    results = advanced_filter.qs
    
    print(f"All products ordered by price (lowest to highest):")
    for product in results:
        print(f"  - {product.name}: ${product.price}")
    
    # Order by stock (descending) - highest stock first
    filter_data = {'ordering': '-stock'}
    advanced_filter = AdvancedProductFilter(filter_data, queryset=Product.objects.all())
    results = advanced_filter.qs
    
    print(f"\nAll products ordered by stock (highest to lowest):")
    for product in results:
        print(f"  - {product.name}: {product.stock} units")


def generate_inventory_report():
    """Generate a comprehensive inventory report using filters."""
    print("\n=== INVENTORY MANAGEMENT REPORT ===")
    
    # Out of stock items (urgent!)
    filter_data = {'out_of_stock': True}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    out_of_stock = product_filter.qs
    
    print(f"🚨 OUT OF STOCK ITEMS ({out_of_stock.count()} items):")
    for product in out_of_stock:
        print(f"  - {product.name} (${product.price})")
    
    # Low stock items (warning)
    filter_data = {'low_stock': 10}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    low_stock = product_filter.qs.exclude(stock=0)  # Exclude out of stock items
    
    print(f"\n⚠️  LOW STOCK ITEMS ({low_stock.count()} items - stock < 10):")
    for product in low_stock:
        print(f"  - {product.name}: {product.stock} units (${product.price})")
    
    # Well-stocked items
    filter_data = {'stock_gte': 10}
    product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
    well_stocked = product_filter.qs
    
    print(f"\n✅ WELL-STOCKED ITEMS ({well_stocked.count()} items - stock >= 10):")
    for product in well_stocked:
        print(f"  - {product.name}: {product.stock} units")
    
    # Value summary
    total_products = Product.objects.count()
    print(f"\n📊 SUMMARY:")
    print(f"  Total products: {total_products}")
    print(f"  Out of stock: {out_of_stock.count()}")
    print(f"  Low stock: {low_stock.count()}")
    print(f"  Well-stocked: {well_stocked.count()}")


def run_all_tests():
    """Run all ProductFilter tests."""
    print("Starting ProductFilter Tests")
    print("=" * 60)
    
    # Create test data
    create_test_products()
    
    # Run individual tests
    test_name_filter()
    test_price_filters()
    test_stock_filters()
    test_low_stock_filter()
    test_stock_availability_filters()
    test_price_category_filter()
    test_combined_filters()
    test_advanced_filter_with_ordering()
    
    # Generate report
    generate_inventory_report()
    
    print("\n" + "=" * 60)
    print("All ProductFilter tests completed!")
    print("\n💡 Key Takeaways:")
    print("  ✅ NumberFilter (not RangeFilter) for gte/lte comparisons")
    print("  ✅ Custom filter methods for complex logic")
    print("  ✅ Meta class is required for FilterSet")
    print("  ✅ Low stock filter answers the challenge question!")


if __name__ == "__main__":
    run_all_tests()
