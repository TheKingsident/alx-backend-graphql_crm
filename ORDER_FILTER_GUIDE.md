# OrderFilter Examples and Usage Guide

This document shows how to use the OrderFilter in your Django-GraphQL project with related field lookups and many-to-many filtering.

## OrderFilter Features ✨

### 1. **Total Amount Range Filters**
```graphql
# Orders with total amount >= $100
query {
  filteredOrders(totalAmountGte: 100.0) {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
  }
}

# Orders between $50 and $500
query {
  filteredOrders(totalAmountGte: 50.0, totalAmountLte: 500.0) {
    id
    totalAmount
    customer {
      name
    }
    products {
      name
      price
    }
  }
}
```

### 2. **Order Date Range Filters**
```graphql
# Orders placed after a specific date
query {
  filteredOrders(orderDateGte: "2024-01-01T00:00:00Z") {
    id
    orderDate
    totalAmount
    customer {
      name
    }
  }
}

# Orders placed within a date range
query {
  filteredOrders(
    orderDateGte: "2024-01-01T00:00:00Z"
    orderDateLte: "2024-12-31T23:59:59Z"
  ) {
    id
    orderDate
    totalAmount
  }
}
```

### 3. **Customer Name Filter (Related Field Lookup)**
```graphql
# Filter orders by customer's name - this demonstrates related field filtering
query {
  filteredOrders(customerName: "john") {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
    products {
      name
    }
  }
}

# Filter by customer email
query {
  filteredOrders(customerEmail: "gmail") {
    id
    customer {
      name
      email
    }
    totalAmount
  }
}
```

### 4. **Product Name Filter (Many-to-Many Related Field)**
```graphql
# Filter orders that contain products with "laptop" in the name
query {
  filteredOrders(productName: "laptop") {
    id
    totalAmount
    customer {
      name
    }
    products {
      name
      price
    }
  }
}
```

### 5. **🎯 CHALLENGE: Filter by Specific Product ID**
```graphql
# Find all orders containing a specific product (by product ID)
query {
  filteredOrders(productId: "123e4567-e89b-12d3-a456-426614174000") {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
    products {
      id
      name
      price
    }
  }
}

# Alternative: More flexible product filter (works with ID or name)
query {
  filteredOrders(containsProduct: "Gaming Laptop") {
    id
    totalAmount
    products {
      name
    }
  }
}

# Or filter by product ID using the flexible filter
query {
  filteredOrders(containsProduct: "123e4567-e89b-12d3-a456-426614174000") {
    id
    totalAmount
    products {
      name
    }
  }
}
```

## Advanced Filtering Examples

### 6. **High-Value Orders**
```graphql
# Filter high-value orders (> $500)
query {
  filteredOrders(highValueOrders: true) {
    id
    totalAmount
    customer {
      name
    }
    products {
      name
      price
    }
  }
}
```

### 7. **Recent Orders**
```graphql
# Orders placed in the last 30 days
query {
  filteredOrders(recentOrders: true) {
    id
    orderDate
    totalAmount
    customer {
      name
    }
  }
}
```

### 8. **Orders by Value Category**
```graphql
# Small orders (< $100)
query {
  filteredOrders(orderValueCategory: "small") {
    id
    totalAmount
    customer {
      name
    }
  }
}

# Enterprise orders (> $1000)
query {
  filteredOrders(orderValueCategory: "enterprise") {
    id
    totalAmount
    customer {
      name
      email
    }
    products {
      name
      price
    }
  }
}
```

### 9. **Orders with Minimum Product Count**
```graphql
# Orders containing at least 3 products
query {
  filteredOrders(minProducts: 3) {
    id
    totalAmount
    customer {
      name
    }
    products {
      name
    }
  }
}
```

## Complex Combined Filters

### 10. **Multi-Criteria Filtering**
```graphql
# High-value orders from customers named "john" containing "laptop" products
query {
  filteredOrders(
    customerName: "john"
    productName: "laptop"
    totalAmountGte: 500.0
    recentOrders: true
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
    products {
      name
      price
    }
  }
}
```

### 11. **Sales Analysis Query**
```graphql
query SalesAnalysis {
  # Recent high-value orders
  recentHighValue: filteredOrders(
    recentOrders: true
    highValueOrders: true
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
    }
  }
  
  # Orders from Gmail customers
  gmailCustomers: filteredOrders(customerEmail: "gmail") {
    id
    totalAmount
    customer {
      email
    }
  }
  
  # Laptop orders
  laptopOrders: filteredOrders(productName: "laptop") {
    id
    totalAmount
    products {
      name
    }
  }
}
```

### 12. **Customer Order History**
```graphql
# All orders from a specific customer
query CustomerOrderHistory($customerId: ID!) {
  filteredOrders(customerId: $customerId) {
    id
    orderDate
    totalAmount
    products {
      name
      price
    }
  }
}
```

## Advanced Filtering with DjangoFilterConnectionField

### 13. **Relay-Style Filtering**
```graphql
query {
  orders(
    customerName_Icontains: "john"
    totalAmount_Gte: 100.0
    productName_Icontains: "laptop"
    first: 10
  ) {
    edges {
      node {
        id
        totalAmount
        orderDate
        customer {
          name
          email
        }
        products {
          name
          price
        }
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
```

## Understanding Related Field Lookups

### Key Concepts:

1. **Single Relationship (ForeignKey)**: `customer__name`
   - Uses double underscore to access related fields
   - Order → Customer (one-to-many relationship)

2. **Many-to-Many Relationship**: `products__name`
   - Also uses double underscore
   - Order → Products (many-to-many relationship)
   - May return duplicates, use `.distinct()` in complex queries

3. **UUID Filtering**: For filtering by ID fields
   - Use `UUIDFilter` for UUID primary keys
   - Important for the product_id challenge filter

## Real-World Use Cases

### 14. **Order Management Dashboard**
```graphql
query OrderManagementDashboard {
  # Recent orders needing attention
  recentOrders: filteredOrders(
    recentOrders: true
    orderValueCategory: "large"
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
      phone
    }
  }
  
  # High-value customers' orders
  highValueOrders: filteredOrders(highValueOrders: true) {
    id
    totalAmount
    customer {
      name
      email
    }
  }
}
```

### 15. **Product Performance Analysis**
```graphql
# Find orders containing a specific product for sales analysis
query ProductPerformance($productId: ID!) {
  ordersWithProduct: filteredOrders(productId: $productId) {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
    products {
      name
      price
    }
  }
}
```

### 16. **Customer Segmentation**
```graphql
query CustomerSegmentation {
  # Premium customers (high-value orders)
  premiumCustomers: filteredOrders(
    orderValueCategory: "enterprise"
    recentOrders: true
  ) {
    customer {
      name
      email
    }
    totalAmount
  }
  
  # Frequent buyers (multiple products per order)
  frequentBuyers: filteredOrders(minProducts: 5) {
    customer {
      name
    }
    products {
      name
    }
  }
}
```

## Tips for Learning

### Understanding the Filter Structure:
1. **Field Name**: Direct model fields (`total_amount`, `order_date`)
2. **Related Fields**: Use `__` to access related model fields (`customer__name`)
3. **Lookup Expressions**: Add suffixes like `__gte`, `__lte`, `__icontains`
4. **Custom Methods**: For complex logic that can't be expressed with simple lookups

### Best Practices:
1. Use `.distinct()` when filtering on many-to-many relationships
2. Consider performance implications of complex related field queries
3. Use indexes on frequently filtered fields
4. Test your filters with realistic data volumes

The OrderFilter demonstrates advanced Django filtering concepts including related field lookups, many-to-many filtering, and custom filter methods. The challenge filter for product ID showcases how to handle UUID filtering in many-to-many relationships!
