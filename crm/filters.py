import django_filters
from django.db.models import Q
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """
    CustomerFilter provides various filtering options for Customer model:
    
    1. name: Case-insensitive partial match using icontains
    2. email: Case-insensitive partial match using icontains  
    3. created_at: Date range filtering with gte and lte
    4. phone_pattern: Custom filter for phone number patterns
    """
    
    # Case-insensitive partial match for name
    # This will match any customer whose name contains the search term (case-insensitive)
    # Example: searching "john" will match "John Doe", "Johnny", "johnson", etc.
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text="Search for customers by name (case-insensitive partial match)"
    )
    
    # Case-insensitive partial match for email
    # This will match any customer whose email contains the search term (case-insensitive)
    # Example: searching "gmail" will match "user@gmail.com", "test.Gmail@example.com", etc.
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        help_text="Search for customers by email (case-insensitive partial match)"
    )
    
    # Date range filters for created_at
    # These allow filtering customers created within a specific date range
    
    # Filter for customers created on or after this date
    created_at_gte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text="Filter customers created on or after this date (YYYY-MM-DD HH:MM:SS)"
    )
    
    # Filter for customers created on or before this date  
    created_at_lte = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text="Filter customers created on or before this date (YYYY-MM-DD HH:MM:SS)"
    )
    
    # Alternative: Date range filter (you can use either approach)
    # This creates a single filter that accepts a date range
    created_at_range = django_filters.DateFromToRangeFilter(
        field_name='created_at',
        help_text="Filter customers created within a date range"
    )
    
    # CHALLENGE: Custom filter for phone number patterns
    # This demonstrates how to create a custom filter method
    phone_pattern = django_filters.CharFilter(
        method='filter_phone_pattern',
        help_text="Custom phone pattern filter (e.g., '+1' for US numbers)"
    )
    
    # Additional useful filters you might want:
    
    # Exact match filters
    name_exact = django_filters.CharFilter(
        field_name='name',
        lookup_expr='exact',
        help_text="Exact name match (case-sensitive)"
    )
    
    # Starts with filter
    name_startswith = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
        help_text="Name starts with (case-insensitive)"
    )
    
    # Email domain filter
    email_domain = django_filters.CharFilter(
        method='filter_email_domain',
        help_text="Filter by email domain (e.g., 'gmail.com')"
    )
    
    class Meta:
        model = Customer
        fields = {
            # You can also define filters directly in Meta.fields
            # This is an alternative approach to defining them as class attributes
            'phone': ['exact', 'icontains'],  # Allows phone and phone__icontains
        }
    
    def filter_phone_pattern(self, queryset, name, value):
        """
        Custom filter method for phone number patterns.
        
        This method demonstrates how to create complex filtering logic.
        It can handle various phone number pattern searches:
        - Starts with: e.g., "+1" for US numbers
        - Contains specific patterns
        - Multiple pattern matching
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name (not used in this case)
            value: The search pattern provided by the user
            
        Returns:
            Filtered QuerySet based on the phone pattern
        """
        if not value:
            return queryset
            
        # Convert to string and strip whitespace
        pattern = str(value).strip()
        
        if not pattern:
            return queryset
        
        # Create a Q object for complex phone pattern matching
        phone_q = Q()
        
        # Check if pattern starts with "+"  
        if pattern.startswith('+'):
            # For patterns like "+1", match phones that start with this
            phone_q |= Q(phone__startswith=pattern)
            
        # Check for common US patterns
        elif pattern.lower() in ['us', 'usa', 'united states']:
            # Match US phone patterns: +1, numbers starting with +1
            phone_q |= Q(phone__startswith='+1')
            
        # Check for other country codes
        elif pattern in ['+44', '+33', '+49', '+86', '+91']:  # UK, France, Germany, China, India
            phone_q |= Q(phone__startswith=pattern)
            
        # For other patterns, do a contains search
        else:
            # This handles partial number searches, area codes, etc.
            phone_q |= Q(phone__icontains=pattern)
            
        # Also check if the pattern appears at the beginning (without +)
        # This handles cases where someone searches "1" to find US numbers
        if pattern.isdigit():
            phone_q |= Q(phone__startswith=f'+{pattern}')
            phone_q |= Q(phone__startswith=pattern)
        
        return queryset.filter(phone_q)
    
    def filter_email_domain(self, queryset, name, value):
        """
        Custom filter for email domains.
        
        This allows filtering customers by their email domain.
        Example: filtering by "gmail.com" will return all customers with @gmail.com emails
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: The domain to search for
            
        Returns:
            Filtered QuerySet containing customers with emails from the specified domain
        """
        if not value:
            return queryset
            
        domain = str(value).strip().lower()
        
        if not domain:
            return queryset
            
        # Ensure domain doesn't start with @
        if domain.startswith('@'):
            domain = domain[1:]
            
        # Filter emails that end with @domain
        return queryset.filter(email__iendswith=f'@{domain}')


# Alternative: More advanced FilterSet with ordering
class AdvancedCustomerFilter(CustomerFilter):
    """
    Extended CustomerFilter with additional features like ordering and more complex filters.
    """
    
    # Ordering filter - allows sorting results
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('email', 'email'), 
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'name': 'Name',
            'email': 'Email',
            'created_at': 'Created Date',
            'updated_at': 'Updated Date',
        },
        help_text="Order results by field (use '-' prefix for descending order)"
    )
    
    # Multiple choice filter example
    has_phone = django_filters.BooleanFilter(
        method='filter_has_phone',
        help_text="Filter customers who have/don't have phone numbers"
    )
    
    def filter_has_phone(self, queryset, name, value):
        """Filter customers based on whether they have a phone number."""
        if value is True:
            return queryset.exclude(phone__isnull=True).exclude(phone__exact='')
        elif value is False:
            return queryset.filter(Q(phone__isnull=True) | Q(phone__exact=''))
        return queryset

class ProductFilter(django_filters.FilterSet):
    """
    ProductFilter provides various filtering options for Product model:
    
    1. name: Case-insensitive partial match using icontains
    2. price: Range filtering with gte and lte for price comparisons
    3. stock: Exact match or range filtering for stock levels
    4. low_stock: Custom filter for products with low stock (< specified value)
    """
    
    # Case-insensitive partial match for product name
    # Example: searching "laptop" will match "Gaming Laptop", "MacBook", etc.
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text="Search for products by name (case-insensitive partial match)"
    )
    
    # Price range filters
    # Use NumberFilter (not RangeFilter) for individual gte/lte comparisons
    price_gte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        help_text="Filter products with price greater than or equal to this value"
    )
    
    price_lte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        help_text="Filter products with price less than or equal to this value"
    )
    
    # Price range filter (alternative approach - single filter for range)
    price_range = django_filters.RangeFilter(
        field_name='price',
        help_text="Filter products within a price range (min_value,max_value)"
    )
    
    # Stock filters
    # Exact stock match
    stock = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='exact',
        help_text="Filter products with exact stock quantity"
    )
    
    # Stock range filters
    stock_gte = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='gte',
        help_text="Filter products with stock greater than or equal to this value"
    )
    
    stock_lte = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='lte',
        help_text="Filter products with stock less than or equal to this value"
    )
    
    # Stock range filter (alternative approach)
    stock_range = django_filters.RangeFilter(
        field_name='stock',
        help_text="Filter products within a stock range (min_stock,max_stock)"
    )
    
    # CHALLENGE: Low stock filter - products with stock below a threshold
    # This is a custom filter that allows you to find products that need restocking
    low_stock = django_filters.NumberFilter(
        method='filter_low_stock',
        help_text="Filter products with stock below this threshold (default: 10)"
    )
    
    # Additional useful filters:
    
    # Out of stock filter
    out_of_stock = django_filters.BooleanFilter(
        method='filter_out_of_stock',
        help_text="Filter products that are out of stock (stock = 0)"
    )
    
    # In stock filter  
    in_stock = django_filters.BooleanFilter(
        method='filter_in_stock',
        help_text="Filter products that are in stock (stock > 0)"
    )
    
    # Price category filters (custom logic)
    price_category = django_filters.ChoiceFilter(
        method='filter_price_category',
        choices=[
            ('budget', 'Budget (< $50)'),
            ('mid-range', 'Mid-range ($50 - $200)'),
            ('premium', 'Premium ($200 - $500)'),
            ('luxury', 'Luxury (> $500)'),
        ],
        help_text="Filter products by price category"
    )
    
    class Meta:
        model = Product
        fields = {
            # Alternative way to define filters in Meta.fields
            # This creates additional filter options automatically
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'gte', 'lte', 'range'],
            'stock': ['exact', 'gte', 'lte', 'range'],
            'created_at': ['gte', 'lte', 'range'],
        }
    
    def filter_low_stock(self, queryset, name, value):
        """
        Custom filter for products with low stock.
        
        This method finds products that have stock below a specified threshold.
        Useful for inventory management and restocking alerts.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name (not used in this case)
            value: The stock threshold (products with stock < this value will be returned)
            
        Returns:
            Filtered QuerySet containing products with low stock
        """
        if value is None:
            # Default threshold of 10 if no value provided
            value = 10
            
        try:
            threshold = int(value)
            return queryset.filter(stock__lt=threshold)
        except (ValueError, TypeError):
            # If invalid value provided, return empty queryset
            return queryset.none()
    
    def filter_out_of_stock(self, queryset, name, value):
        """
        Filter for products that are completely out of stock.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: Boolean value (True for out of stock, False for in stock)
            
        Returns:
            Filtered QuerySet based on stock availability
        """
        if value is True:
            return queryset.filter(stock=0)
        elif value is False:
            return queryset.filter(stock__gt=0)
        return queryset
    
    def filter_in_stock(self, queryset, name, value):
        """
        Filter for products that are in stock.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: Boolean value (True for in stock, False for out of stock)
            
        Returns:
            Filtered QuerySet based on stock availability
        """
        if value is True:
            return queryset.filter(stock__gt=0)
        elif value is False:
            return queryset.filter(stock=0)
        return queryset
    
    def filter_price_category(self, queryset, name, value):
        """
        Custom filter for price categories.
        
        This demonstrates how to create categorical filters based on ranges.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: The price category choice
            
        Returns:
            Filtered QuerySet containing products in the specified price category
        """
        if value == 'budget':
            return queryset.filter(price__lt=50)
        elif value == 'mid-range':
            return queryset.filter(price__gte=50, price__lt=200)
        elif value == 'premium':
            return queryset.filter(price__gte=200, price__lt=500)
        elif value == 'luxury':
            return queryset.filter(price__gte=500)
        return queryset


# Advanced ProductFilter with ordering and more features
class AdvancedProductFilter(ProductFilter):
    """
    Extended ProductFilter with additional features like ordering and complex filters.
    """
    
    # Ordering filter - allows sorting results
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('price', 'price'),
            ('stock', 'stock'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'name': 'Product Name',
            'price': 'Price',
            'stock': 'Stock Quantity',
            'created_at': 'Created Date',
            'updated_at': 'Updated Date',
        },
        help_text="Order results by field (use '-' prefix for descending order)"
    )
    
    # Search filter that searches across multiple fields
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search across product name and description"
    )
    
    def filter_search(self, queryset, name, value):
        """
        Search across multiple fields.
        
        This allows searching for products by name or any other relevant field.
        """
        if not value:
            return queryset
            
        search_term = str(value).strip()
        if not search_term:
            return queryset
            
        # Search in name field (you can add more fields as needed)
        return queryset.filter(
            Q(name__icontains=search_term)
            # Add more fields here when available, e.g.:
            # | Q(description__icontains=search_term)
            # | Q(category__name__icontains=search_term)
        )

class OrderFilter(django_filters.FilterSet):
    """
    OrderFilter provides various filtering options for Order model:
    
    1. total_amount: Range filtering with gte and lte for amount comparisons
    2. order_date: Date range filtering for order dates
    3. customer_name: Filter by customer's name using related field lookup
    4. product_name: Filter by product's name using related field lookup
    5. product_id: CHALLENGE - Filter orders containing a specific product ID
    """
    
    # Total amount range filters
    # Use NumberFilter for individual gte/lte comparisons on decimal fields
    total_amount_gte = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='gte',
        help_text="Filter orders with total amount greater than or equal to this value"
    )
    
    total_amount_lte = django_filters.NumberFilter(
        field_name='total_amount',
        lookup_expr='lte',
        help_text="Filter orders with total amount less than or equal to this value"
    )
    
    # Total amount range filter (alternative approach)
    total_amount_range = django_filters.RangeFilter(
        field_name='total_amount',
        help_text="Filter orders within a total amount range (min_amount,max_amount)"
    )
    
    # Order date range filters
    # Filter for orders placed on or after this date
    order_date_gte = django_filters.DateTimeFilter(
        field_name='order_date',
        lookup_expr='gte',
        help_text="Filter orders placed on or after this date (YYYY-MM-DD HH:MM:SS)"
    )
    
    # Filter for orders placed on or before this date
    order_date_lte = django_filters.DateTimeFilter(
        field_name='order_date',
        lookup_expr='lte',
        help_text="Filter orders placed on or before this date (YYYY-MM-DD HH:MM:SS)"
    )
    
    # Order date range filter (alternative approach)
    order_date_range = django_filters.DateFromToRangeFilter(
        field_name='order_date',
        help_text="Filter orders within a date range"
    )
    
    # RELATED FIELD LOOKUP: Filter by customer's name
    # This demonstrates how to filter across relationships
    # The double underscore (__) syntax accesses related fields
    customer_name = django_filters.CharFilter(
        field_name='customer__name',  # Access the customer's name field
        lookup_expr='icontains',
        help_text="Filter orders by customer's name (case-insensitive partial match)"
    )
    
    # Additional customer filters
    customer_email = django_filters.CharFilter(
        field_name='customer__email',
        lookup_expr='icontains',
        help_text="Filter orders by customer's email (case-insensitive partial match)"
    )
    
    # MANY-TO-MANY RELATED FIELD LOOKUP: Filter by product's name
    # This is more complex because orders have a many-to-many relationship with products
    product_name = django_filters.CharFilter(
        field_name='products__name',  # Access the products' name field
        lookup_expr='icontains',
        help_text="Filter orders by product's name (case-insensitive partial match)"
    )
    
    # CHALLENGE: Filter orders that include a specific product ID
    # This demonstrates filtering on many-to-many relationships by ID
    product_id = django_filters.UUIDFilter(
        field_name='products__id',  # Access the products' ID field
        help_text="Filter orders that contain a specific product ID"
    )
    
    # Alternative method using custom filter for product ID (more flexible)
    contains_product = django_filters.CharFilter(
        method='filter_contains_product',
        help_text="Filter orders containing a specific product (by ID or name)"
    )
    
    # Additional useful filters:
    
    # Filter by customer ID
    customer_id = django_filters.UUIDFilter(
        field_name='customer__id',
        help_text="Filter orders by specific customer ID"
    )
    
    # Filter orders with high/low amounts
    high_value_orders = django_filters.BooleanFilter(
        method='filter_high_value_orders',
        help_text="Filter high-value orders (> $500 by default)"
    )
    
    # Filter recent orders
    recent_orders = django_filters.BooleanFilter(
        method='filter_recent_orders',
        help_text="Filter orders placed in the last 30 days"
    )
    
    # Filter orders by number of products
    min_products = django_filters.NumberFilter(
        method='filter_min_products',
        help_text="Filter orders containing at least this many products"
    )
    
    # Order status simulation (if you had a status field)
    order_value_category = django_filters.ChoiceFilter(
        method='filter_order_value_category',
        choices=[
            ('small', 'Small Orders (< $100)'),
            ('medium', 'Medium Orders ($100 - $500)'),
            ('large', 'Large Orders ($500 - $1000)'),
            ('enterprise', 'Enterprise Orders (> $1000)'),
        ],
        help_text="Filter orders by value category"
    )
    
    class Meta:
        model = Order
        fields = {
            # Alternative way to define filters in Meta.fields
            # This creates additional filter options automatically
            'total_amount': ['exact', 'gte', 'lte', 'range'],
            'order_date': ['exact', 'gte', 'lte', 'date', 'range'],
            'created_at': ['gte', 'lte', 'range'],
            # Related field filters can also be defined here
            'customer__name': ['exact', 'icontains'],
            'customer__email': ['exact', 'icontains'],
            'products__name': ['exact', 'icontains'],
            'products__id': ['exact'],
        }
    
    def filter_contains_product(self, queryset, name, value):
        """
        Custom filter for orders containing a specific product.
        
        This method allows filtering by product ID or product name,
        demonstrating flexible filtering on many-to-many relationships.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name (not used in this case)
            value: The product identifier (ID or name)
            
        Returns:
            Filtered QuerySet containing orders with the specified product
        """
        if not value:
            return queryset
            
        search_term = str(value).strip()
        if not search_term:
            return queryset
        
        # Try to find by UUID first (if it looks like a UUID)
        try:
            import uuid
            product_uuid = uuid.UUID(search_term)
            return queryset.filter(products__id=product_uuid)
        except (ValueError, AttributeError):
            # If not a valid UUID, search by product name
            return queryset.filter(products__name__icontains=search_term)
    
    def filter_high_value_orders(self, queryset, name, value):
        """
        Filter for high-value orders.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: Boolean value (True for high-value orders)
            
        Returns:
            Filtered QuerySet based on order value
        """
        if value is True:
            # Orders with total amount > $500 (you can adjust this threshold)
            return queryset.filter(total_amount__gt=500)
        elif value is False:
            return queryset.filter(total_amount__lte=500)
        return queryset
    
    def filter_recent_orders(self, queryset, name, value):
        """
        Filter for recent orders (last 30 days).
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: Boolean value (True for recent orders)
            
        Returns:
            Filtered QuerySet based on order recency
        """
        if value is True:
            from django.utils import timezone
            from datetime import timedelta
            
            thirty_days_ago = timezone.now() - timedelta(days=30)
            return queryset.filter(order_date__gte=thirty_days_ago)
        elif value is False:
            from django.utils import timezone
            from datetime import timedelta
            
            thirty_days_ago = timezone.now() - timedelta(days=30)
            return queryset.filter(order_date__lt=thirty_days_ago)
        return queryset
    
    def filter_min_products(self, queryset, name, value):
        """
        Filter orders containing at least a specified number of products.
        
        This demonstrates how to filter based on aggregated data
        from many-to-many relationships.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: Minimum number of products
            
        Returns:
            Filtered QuerySet containing orders with at least the specified number of products
        """
        if value is None:
            return queryset
            
        try:
            min_count = int(value)
            from django.db.models import Count
            
            # Annotate with product count and filter
            return queryset.annotate(
                product_count=Count('products')
            ).filter(product_count__gte=min_count)
        except (ValueError, TypeError):
            return queryset.none()
    
    def filter_order_value_category(self, queryset, name, value):
        """
        Custom filter for order value categories.
        
        This demonstrates how to create categorical filters based on ranges.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: The order value category choice
            
        Returns:
            Filtered QuerySet containing orders in the specified value category
        """
        if value == 'small':
            return queryset.filter(total_amount__lt=100)
        elif value == 'medium':
            return queryset.filter(total_amount__gte=100, total_amount__lt=500)
        elif value == 'large':
            return queryset.filter(total_amount__gte=500, total_amount__lt=1000)
        elif value == 'enterprise':
            return queryset.filter(total_amount__gte=1000)
        return queryset


# Advanced OrderFilter with ordering and more features
class AdvancedOrderFilter(OrderFilter):
    """
    Extended OrderFilter with additional features like ordering and complex filters.
    """
    
    # Ordering filter - allows sorting results
    ordering = django_filters.OrderingFilter(
        fields=(
            ('order_date', 'order_date'),
            ('total_amount', 'total_amount'),
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('customer__name', 'customer_name'),  # Order by customer name
        ),
        field_labels={
            'order_date': 'Order Date',
            'total_amount': 'Total Amount',
            'created_at': 'Created Date',
            'updated_at': 'Updated Date',
            'customer_name': 'Customer Name',
        },
        help_text="Order results by field (use '-' prefix for descending order)"
    )
    
    # Advanced search filter that searches across multiple related fields
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search across customer name, email, and product names"
    )
    
    # Filter by multiple product IDs
    product_ids = django_filters.CharFilter(
        method='filter_product_ids',
        help_text="Filter orders containing any of the specified product IDs (comma-separated)"
    )
    
    def filter_search(self, queryset, name, value):
        """
        Search across multiple related fields.
        
        This allows searching for orders by customer information or product names.
        """
        if not value:
            return queryset
            
        search_term = str(value).strip()
        if not search_term:
            return queryset
            
        # Search across customer and product fields
        return queryset.filter(
            Q(customer__name__icontains=search_term) |
            Q(customer__email__icontains=search_term) |
            Q(products__name__icontains=search_term)
        ).distinct()  # Use distinct() to avoid duplicates from many-to-many joins
    
    def filter_product_ids(self, queryset, name, value):
        """
        Filter orders containing any of the specified product IDs.
        
        This allows filtering by multiple product IDs in a single query.
        
        Args:
            queryset: The current QuerySet being filtered
            name: The filter field name
            value: Comma-separated list of product IDs
            
        Returns:
            Filtered QuerySet containing orders with any of the specified products
        """
        if not value:
            return queryset
            
        try:
            import uuid
            # Split by comma and clean up
            product_id_strings = [pid.strip() for pid in str(value).split(',') if pid.strip()]
            product_uuids = []
            
            # Convert to UUIDs
            for pid_str in product_id_strings:
                try:
                    product_uuids.append(uuid.UUID(pid_str))
                except ValueError:
                    continue  # Skip invalid UUIDs
            
            if product_uuids:
                return queryset.filter(products__id__in=product_uuids).distinct()
            
        except Exception:
            pass
            
        return queryset.none()
