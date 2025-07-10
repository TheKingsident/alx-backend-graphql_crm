"""
Test file for CustomerFilter functionality.

This file demonstrates how to test the filters and provides examples
of how the filtering works with actual data.
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append('/home/cakemurderer/ALX_Projects/alx_backend_graphql')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Customer
from crm.filters import CustomerFilter, AdvancedCustomerFilter
from django.utils import timezone
from datetime import datetime, timedelta


def create_test_customers():
    """Create test customers for filter testing."""
    print("Creating test customers...")
    
    test_customers = [
        {
            'name': 'John Doe',
            'email': 'john.doe@gmail.com',
            'phone': '+1234567890'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane.smith@yahoo.com',
            'phone': '+1987654321'
        },
        {
            'name': 'Bob Johnson',
            'email': 'bob.johnson@gmail.com',
            'phone': '+44123456789'
        },
        {
            'name': 'Alice Brown',
            'email': 'alice.brown@hotmail.com',
            'phone': None
        },
        {
            'name': 'Charlie Wilson',
            'email': 'charlie@company.com',
            'phone': '+33123456789'
        },
        {
            'name': 'David Lee',
            'email': 'david.lee@gmail.com',
            'phone': '555-123-4567'
        }
    ]
    
    for customer_data in test_customers:
        customer, created = Customer.objects.get_or_create(
            email=customer_data['email'],
            defaults=customer_data
        )
        if created:
            print(f"Created: {customer.name}")
        else:
            print(f"Already exists: {customer.name}")
    
    print(f"Total customers in database: {Customer.objects.count()}")


def test_name_filter():
    """Test the name filter with case-insensitive partial matching."""
    print("\n=== Testing Name Filter ===")
    
    # Test case-insensitive partial match
    filter_data = {'name': 'john'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"Searching for name containing 'john':")
    for customer in results:
        print(f"  - {customer.name} ({customer.email})")
    
    # Test exact match
    filter_data = {'name_exact': 'John Doe'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nSearching for exact name 'John Doe':")
    for customer in results:
        print(f"  - {customer.name} ({customer.email})")


def test_email_filter():
    """Test the email filter with case-insensitive partial matching."""
    print("\n=== Testing Email Filter ===")
    
    # Test partial email match
    filter_data = {'email': 'gmail'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"Searching for emails containing 'gmail':")
    for customer in results:
        print(f"  - {customer.name} ({customer.email})")
    
    # Test email domain filter
    filter_data = {'email_domain': 'gmail.com'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nSearching for email domain 'gmail.com':")
    for customer in results:
        print(f"  - {customer.name} ({customer.email})")


def test_date_filter():
    """Test the date range filtering."""
    print("\n=== Testing Date Filter ===")
    
    # Get current time and create date range
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)
    
    # Test created_at_gte (customers created after yesterday)
    filter_data = {'created_at_gte': yesterday}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"Customers created after {yesterday.strftime('%Y-%m-%d %H:%M:%S')}:")
    for customer in results:
        print(f"  - {customer.name} (created: {customer.created_at.strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Test created_at_lte (customers created before tomorrow)
    filter_data = {'created_at_lte': tomorrow}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nCustomers created before {tomorrow.strftime('%Y-%m-%d %H:%M:%S')}:")
    print(f"Count: {results.count()}")


def test_phone_pattern_filter():
    """Test the custom phone pattern filter."""
    print("\n=== Testing Phone Pattern Filter ===")
    
    # Test US phone pattern (+1)
    filter_data = {'phone_pattern': '+1'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"Customers with US phone numbers (starting with +1):")
    for customer in results:
        print(f"  - {customer.name} ({customer.phone})")
    
    # Test UK phone pattern (+44)
    filter_data = {'phone_pattern': '+44'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nCustomers with UK phone numbers (starting with +44):")
    for customer in results:
        print(f"  - {customer.name} ({customer.phone})")
    
    # Test area code pattern (555)
    filter_data = {'phone_pattern': '555'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nCustomers with phone numbers containing '555':")
    for customer in results:
        print(f"  - {customer.name} ({customer.phone})")
    
    # Test US keyword search
    filter_data = {'phone_pattern': 'us'}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nCustomers with US phone numbers (using 'us' keyword):")
    for customer in results:
        print(f"  - {customer.name} ({customer.phone})")


def test_has_phone_filter():
    """Test the has_phone boolean filter."""
    print("\n=== Testing Has Phone Filter ===")
    
    # Test customers with phone numbers
    filter_data = {'has_phone': True}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"Customers with phone numbers:")
    for customer in results:
        print(f"  - {customer.name} ({customer.phone})")
    
    # Test customers without phone numbers
    filter_data = {'has_phone': False}
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"\nCustomers without phone numbers:")
    for customer in results:
        print(f"  - {customer.name} (phone: {customer.phone})")


def test_combined_filters():
    """Test combining multiple filters."""
    print("\n=== Testing Combined Filters ===")
    
    # Combine name and email filters
    filter_data = {
        'name': 'john',
        'email': 'gmail',
        'phone_pattern': '+1'
    }
    customer_filter = CustomerFilter(filter_data, queryset=Customer.objects.all())
    results = customer_filter.qs
    
    print(f"Customers with name containing 'john', email containing 'gmail', and US phone:")
    for customer in results:
        print(f"  - {customer.name} ({customer.email}) - {customer.phone}")


def test_advanced_filter_with_ordering():
    """Test the advanced filter with ordering."""
    print("\n=== Testing Advanced Filter with Ordering ===")
    
    # Test ordering by name
    filter_data = {'ordering': 'name'}
    advanced_filter = AdvancedCustomerFilter(filter_data, queryset=Customer.objects.all())
    results = advanced_filter.qs
    
    print(f"All customers ordered by name (ascending):")
    for customer in results:
        print(f"  - {customer.name}")
    
    # Test ordering by creation date (descending)
    filter_data = {'ordering': '-created_at'}
    advanced_filter = AdvancedCustomerFilter(filter_data, queryset=Customer.objects.all())
    results = advanced_filter.qs
    
    print(f"\nAll customers ordered by creation date (newest first):")
    for customer in results:
        print(f"  - {customer.name} (created: {customer.created_at.strftime('%Y-%m-%d %H:%M:%S')})")


def run_all_tests():
    """Run all filter tests."""
    print("Starting CustomerFilter Tests")
    print("=" * 50)
    
    # Create test data
    create_test_customers()
    
    # Run individual tests
    test_name_filter()
    test_email_filter()
    test_date_filter()
    test_phone_pattern_filter()
    test_has_phone_filter()
    test_combined_filters()
    test_advanced_filter_with_ordering()
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    run_all_tests()
