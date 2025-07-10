# ProductFilter Examples and Usage Guide

This document shows how to use the ProductFilter in your Django-GraphQL project.

## What You Did Right ✅

1. **Correct Structure**: You created a `ProductFilter` class extending `django_filters.FilterSet`
2. **Good Filter Names**: Used descriptive names like `price_gte`, `stock_lte`
3. **Help Text**: Added helpful descriptions for each filter
4. **Right Approach**: Implemented both individual filters and range filters

## What Was Fixed 🔧

1. **Filter Types**: Changed `RangeFilter` to `NumberFilter` for individual comparisons (`gte`, `lte`)
2. **Added Meta Class**: Included `Meta` class with `model = Product`
3. **Added Custom Filters**: Implemented the low stock filter and other useful filters
4. **Import Statement**: Added `Product` to the imports

## How Your Filters Work

### 1. Name Filter (Case-insensitive partial match)
```graphql
query {
  filteredProducts(name: "laptop") {
    id
    name
    price
    stock
  }
}
```
This finds products with "laptop" anywhere in the name (case-insensitive).

### 2. Price Range Filters

#### Individual Price Filters:
```graphql
# Products with price >= $100
query {
  filteredProducts(priceGte: 100.0) {
    id
    name
    price
    stock
  }
}

# Products with price <= $500
query {
  filteredProducts(priceLte: 500.0) {
    id
    name
    price
    stock
  }
}

# Products between $100 and $500
query {
  filteredProducts(priceGte: 100.0, priceLte: 500.0) {
    id
    name
    price
    stock
  }
}
```

### 3. Stock Filters

#### Exact Stock Match:
```graphql
query {
  filteredProducts(stock: 5) {
    id
    name
    stock
  }
}
```

#### Stock Range Filters:
```graphql
# Products with at least 10 in stock
query {
  filteredProducts(stockGte: 10) {
    id
    name
    stock
  }
}

# Products with 50 or fewer in stock
query {
  filteredProducts(stockLte: 50) {
    id
    name
    stock
  }
}
```

### 4. Low Stock Filter (Your Challenge Answer! 🎯)

This is the answer to your question "How can you filter products with low stock (e.g., stock < 10)?"

```graphql
# Products with stock below 10 (default threshold)
query {
  filteredProducts(lowStock: 10) {
    id
    name
    stock
    price
  }
}

# Products with stock below 5
query {
  filteredProducts(lowStock: 5) {
    id
    name
    stock
    price
  }
}
```

### 5. Out of Stock / In Stock Filters

```graphql
# Products that are completely out of stock
query {
  filteredProducts(outOfStock: true) {
    id
    name
    stock
  }
}

# Products that are in stock
query {
  filteredProducts(inStock: true) {
    id
    name
    stock
  }
}
```

### 6. Price Category Filter

```graphql
# Budget products (< $50)
query {
  filteredProducts(priceCategory: "budget") {
    id
    name
    price
  }
}

# Premium products ($200 - $500)
query {
  filteredProducts(priceCategory: "premium") {
    id
    name
    price
  }
}
```

### 7. Combined Filters

```graphql
# Low stock, budget laptops
query {
  filteredProducts(
    name: "laptop"
    priceCategory: "budget"
    lowStock: 5
  ) {
    id
    name
    price
    stock
  }
}

# In-stock products under $200
query {
  filteredProducts(
    inStock: true
    priceLte: 200.0
  ) {
    id
    name
    price
    stock
  }
}
```

## Understanding the Filter Types

### NumberFilter vs RangeFilter

**NumberFilter** (What you should use for gte/lte):
- For single value comparisons
- Examples: `price_gte`, `stock_lte`
- Usage: `priceGte: 100.0`

**RangeFilter** (What you should use for ranges):
- For range inputs (min,max)  
- Examples: `price_range`, `stock_range`
- Usage: `priceRange: {min: 100.0, max: 500.0}`

### Custom Filter Methods

Your custom filters use the `method` parameter:

```python
low_stock = django_filters.NumberFilter(
    method='filter_low_stock',
    help_text="Filter products with stock below this threshold"
)

def filter_low_stock(self, queryset, name, value):
    if value is None:
        value = 10  # Default threshold
    return queryset.filter(stock__lt=value)
```

## Real-World Use Cases

### 1. Inventory Management Dashboard
```graphql
query InventoryAlerts {
  lowStockProducts: filteredProducts(lowStock: 10) {
    id
    name
    stock
    price
  }
  
  outOfStockProducts: filteredProducts(outOfStock: true) {
    id
    name
    price
  }
}
```

### 2. E-commerce Product Search
```graphql
query ProductSearch {
  laptops: filteredProducts(
    name: "laptop"
    priceGte: 500.0
    priceLte: 2000.0
    inStock: true
  ) {
    id
    name
    price
    stock
  }
}
```

### 3. Sales Report Filters
```graphql
query SalesAnalysis {
  budgetProducts: filteredProducts(priceCategory: "budget") {
    id
    name
    price
    stock
  }
  
  premiumProducts: filteredProducts(priceCategory: "premium") {
    id
    name
    price
    stock
  }
}
```

## Testing Your Filters

Create a simple test script to verify your filters work:

```python
# test_product_filters.py
from crm.filters import ProductFilter
from crm.models import Product

# Test low stock filter
filter_data = {'low_stock': 10}
product_filter = ProductFilter(filter_data, queryset=Product.objects.all())
low_stock_products = product_filter.qs

print("Low stock products:")
for product in low_stock_products:
    print(f"- {product.name}: {product.stock} units")
```

## Next Steps for Learning

1. **Add Order Filtering**: Create filters for the Order model
2. **Advanced Searches**: Implement full-text search across multiple fields
3. **Aggregation Filters**: Filter by calculated fields (e.g., total order value)
4. **Date Filters**: Add creation date, update date filtering for products

You're definitely on the right track! The concepts you applied are correct, and with these fixes, your ProductFilter will work perfectly with GraphQL queries.
