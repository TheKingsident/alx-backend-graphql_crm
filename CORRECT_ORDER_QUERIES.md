# CORRECT Order Filter Queries

## ❌ Common Wrong Query Patterns:
```graphql
# This WON'T work - same pattern as your previous queries
query {
  allOrders(filter: { 
    totalAmountGte: 500, 
    customerName: "John",
    productName: "laptop" 
  }, orderBy: "-orderDate") {
    edges {
      node {
        id
        totalAmount
        orderDate
        customer {
          name
        }
        products {
          name
        }
      }
    }
  }
}
```

## Problems:
1. `allOrders` doesn't accept any arguments
2. `filter` argument doesn't exist
3. `orderBy` argument doesn't exist on this field
4. `edges/node` structure only works with Connection fields

## ✅ CORRECT Order Queries:

### Option 1: Using `filteredOrders` (Recommended)
```graphql
query {
  filteredOrders(
    totalAmountGte: 500.0
    customerName: "John"
    productName: "laptop"
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

### Option 2: Using `orders` (DjangoFilterConnectionField - Relay Style)
```graphql
query {
  orders(
    totalAmount_Gte: 500.0
    customer__name_Icontains: "John"
    products__name_Icontains: "laptop"
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
    }
  }
}
```

### Option 3: Advanced Filtering with Ordering
```graphql
query {
  # Using AdvancedOrderFilter if available in schema
  advancedFilteredOrders(
    totalAmountGte: 500.0
    customerName: "John"
    productName: "laptop"
    ordering: "-orderDate"
    limit: 10
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

## Complete Order Filter Examples:

### 1. Filter by Total Amount Range
```graphql
query {
  filteredOrders(
    totalAmountGte: 100.0
    totalAmountLte: 2000.0
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
    }
  }
}
```

### 2. Filter by Date Range
```graphql
query {
  filteredOrders(
    orderDateGte: "2025-01-01T00:00:00Z"
    orderDateLte: "2025-12-31T23:59:59Z"
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
    }
  }
}
```

### 3. Filter by Customer Name (Related Field)
```graphql
query {
  filteredOrders(customerName: "John") {
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
```

### 4. Filter by Customer Email Domain
```graphql
query {
  filteredOrders(customerEmail: "gmail") {
    id
    totalAmount
    customer {
      name
      email
    }
  }
}
```

### 5. Filter by Product Name (Many-to-Many)
```graphql
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

### 6. 🎯 CHALLENGE: Filter by Specific Product ID
```graphql
query {
  filteredOrders(productId: "123e4567-e89b-12d3-a456-426614174000") {
    id
    totalAmount
    customer {
      name
    }
    products {
      id
      name
      price
    }
  }
}
```

### 7. Filter by Customer ID
```graphql
query {
  filteredOrders(customerId: "987fcdeb-51a2-43d7-8912-123456789abc") {
    id
    totalAmount
    orderDate
    products {
      name
      price
    }
  }
}
```

### 8. High-Value Orders
```graphql
query {
  filteredOrders(highValueOrders: true) {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
  }
}
```

### 9. Recent Orders (Last 30 Days)
```graphql
query {
  filteredOrders(recentOrders: true) {
    id
    totalAmount
    orderDate
    customer {
      name
    }
  }
}
```

### 10. Orders with Minimum Product Count
```graphql
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

### 11. Orders by Value Category
```graphql
query {
  # Small orders (< $100)
  smallOrders: filteredOrders(orderValueCategory: "small") {
    id
    totalAmount
    customer {
      name
    }
  }
  
  # Enterprise orders (> $1000)
  enterpriseOrders: filteredOrders(orderValueCategory: "enterprise") {
    id
    totalAmount
    customer {
      name
    }
  }
}
```

## Complex Combined Filters:

### 12. Multi-Criteria Business Queries
```graphql
query BusinessIntelligence {
  # High-value recent orders from Gmail customers
  premiumRecentOrders: filteredOrders(
    customerEmail: "gmail"
    highValueOrders: true
    recentOrders: true
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
  }
  
  # Laptop orders from customers named John
  johnLaptopOrders: filteredOrders(
    customerName: "john"
    productName: "laptop"
  ) {
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

### 13. Sales Analysis Query
```graphql
query SalesAnalysis {
  # Recent high-value orders
  recentHighValue: filteredOrders(
    recentOrders: true
    totalAmountGte: 1000.0
  ) {
    id
    totalAmount
    orderDate
    customer {
      name
    }
  }
  
  # Orders with many products (bulk buyers)
  bulkOrders: filteredOrders(minProducts: 5) {
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

### 14. Customer Order History
```graphql
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

### 15. Product Performance Analysis
```graphql
query ProductPerformance($productId: ID!) {
  # All orders containing this product
  productOrders: filteredOrders(productId: $productId) {
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

## Available Order Query Fields in Your Schema:

1. `allOrders` - Simple list, NO filtering ❌
2. `orders` - Connection field with auto-generated filters ✅  
3. `filteredOrders` - List with manual filter arguments ✅

## Available Filter Arguments for `filteredOrders`:

### Amount Filters:
- `totalAmountGte` - Float (total amount greater than or equal)
- `totalAmountLte` - Float (total amount less than or equal)

### Date Filters:
- `orderDateGte` - DateTime (ordered on or after)
- `orderDateLte` - DateTime (ordered on or before)

### Customer Filters (Related Field):
- `customerName` - String (customer name contains)
- `customerEmail` - String (customer email contains)
- `customerId` - ID (specific customer)

### Product Filters (Many-to-Many):
- `productName` - String (product name contains)
- `productId` - ID (specific product - CHALLENGE filter!)
- `containsProduct` - String (flexible product search by ID or name)

### Custom Business Logic Filters:
- `highValueOrders` - Boolean (orders > $500)
- `recentOrders` - Boolean (last 30 days)
- `minProducts` - Int (minimum number of products)
- `orderValueCategory` - String (small, medium, large, enterprise)

### Pagination:
- `limit` - Int (limit results)
- `offset` - Int (pagination offset)

## Available Filters for `orders` (Connection):

The `orders` field uses auto-generated filters:
- `totalAmount_Gte`, `totalAmount_Lte` - Float
- `orderDate_Gte`, `orderDate_Lte` - DateTime
- `customer__name_Icontains` - String
- `customer__email_Icontains` - String
- `products__name_Icontains` - String
- `products__id_Exact` - ID
- Plus pagination: `first`, `last`, `before`, `after`

## Real-World Order Management Queries:

### Order Dashboard:
```graphql
query OrderDashboard {
  # Today's high-value orders
  todayHighValue: filteredOrders(
    orderDateGte: "2025-07-10T00:00:00Z"
    highValueOrders: true
  ) {
    id
    totalAmount
    customer {
      name
      phone
    }
  }
  
  # Recent orders needing attention
  recentLargeOrders: filteredOrders(
    recentOrders: true
    minProducts: 3
  ) {
    id
    totalAmount
    customer {
      name
      email
    }
  }
}
```

### Customer Support Queries:
```graphql
query CustomerSupport {
  # Find orders for customer support
  johnOrders: filteredOrders(customerName: "john") {
    id
    totalAmount
    orderDate
    products {
      name
    }
  }
}
```

### Inventory Impact Analysis:
```graphql
query InventoryImpact {
  # Orders containing laptops (for inventory planning)
  laptopOrders: filteredOrders(productName: "laptop") {
    id
    totalAmount
    orderDate
    products {
      name
      price
    }
  }
}
```

## Using Connection Field with Advanced Filters:
```graphql
query {
  orders(
    totalAmount_Gte: 500.0
    customer__name_Icontains: "john"
    products__name_Icontains: "laptop"
    orderDate_Gte: "2025-01-01T00:00:00Z"
    first: 20
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

## Quick Reference - Field Name Mapping:

| Wrong (Won't Work) | Correct Options |
|-------------------|----------------|
| `allOrders` | `filteredOrders` or `orders` |
| `filter: { totalAmountGte: 500 }` | `totalAmountGte: 500.0` |
| `orderBy: "-orderDate"` | Use `orders` Connection or advanced filter |
| `customerName: "John"` | `customerName: "John"` (manual) or `customer__name_Icontains: "John"` (Connection) |

## Summary:

The Order filtering system demonstrates the most advanced concepts:
- ✅ Related field lookups (`customer__name`)
- ✅ Many-to-many filtering (`products__name`, `products__id`)
- ✅ Custom business logic filters
- ✅ UUID filtering for the challenge requirement
- ✅ Complex multi-criteria filtering for real business use cases

Orders are the most complex because they involve relationships with both Customers and Products, making them perfect for learning advanced Django filtering techniques!
