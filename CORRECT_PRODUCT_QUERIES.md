# CORRECT Product Filter Queries

## ❌ Your Query (Won't Work):
```graphql
query {
  allProducts(filter: { priceGte: 100, priceLte: 1000 }, orderBy: "-stock") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

## Problems:
1. `allProducts` doesn't accept any arguments
2. `filter` argument doesn't exist
3. `orderBy` argument doesn't exist on this field
4. `edges/node` structure only works with Connection fields

## ✅ CORRECT Product Queries:

### Option 1: Using `filteredProducts` (Recommended)
```graphql
query {
  filteredProducts(
    priceGte: 100.0
    priceLte: 1000.0
  ) {
    id
    name
    price
    stock
  }
}
```

### Option 2: Using `products` (DjangoFilterConnectionField - Relay Style)
```graphql
query {
  products(
    price_Gte: 100.0
    price_Lte: 1000.0
    orderBy: "-stock"
    first: 10
  ) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
  }
}
```

### Option 3: Advanced Filtering with Ordering (Using AdvancedProductFilter)
```graphql
query {
  # Note: This would need to be added to your schema if not already there
  advancedFilteredProducts(
    priceGte: 100.0
    priceLte: 1000.0
    ordering: "-stock"
    limit: 10
  ) {
    id
    name
    price
    stock
  }
}
```

## Complete Product Filter Examples:

### 1. Price Range with Stock Filters
```graphql
query {
  filteredProducts(
    priceGte: 100.0
    priceLte: 1000.0
    stockGte: 5
  ) {
    id
    name
    price
    stock
  }
}
```

### 2. Low Stock Products in Price Range
```graphql
query {
  filteredProducts(
    priceGte: 100.0
    priceLte: 1000.0
    lowStock: 10
  ) {
    id
    name
    price
    stock
  }
}
```

### 3. Filter by Name and Price Category
```graphql
query {
  filteredProducts(
    name: "laptop"
    priceCategory: "premium"
  ) {
    id
    name
    price
    stock
  }
}
```

### 4. In-Stock Products with Price Range
```graphql
query {
  filteredProducts(
    priceGte: 100.0
    priceLte: 1000.0
    inStock: true
  ) {
    id
    name
    price
    stock
  }
}
```

### 5. Using Connection Field with Pagination and Sorting
```graphql
query {
  products(
    price_Gte: 100.0
    price_Lte: 1000.0
    stock_Gte: 5
    first: 20
  ) {
    edges {
      node {
        id
        name
        price
        stock
        createdAt
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

## Available Product Query Fields in Your Schema:

1. `allProducts` - Simple list, NO filtering ❌
2. `products` - Connection field with auto-generated filters ✅  
3. `filteredProducts` - List with manual filter arguments ✅

## Available Filter Arguments for `filteredProducts`:

- `name` - String (case-insensitive partial match)
- `priceGte` - Float (price greater than or equal)
- `priceLte` - Float (price less than or equal)
- `stock` - Int (exact stock quantity)
- `stockGte` - Int (stock greater than or equal)
- `stockLte` - Int (stock less than or equal)
- `lowStock` - Int (stock below threshold)
- `outOfStock` - Boolean (stock = 0)
- `inStock` - Boolean (stock > 0)
- `priceCategory` - String (budget, mid-range, premium, luxury)
- `limit` - Int (pagination)
- `offset` - Int (pagination)

## Available Filters for `products` (Connection):

The `products` field uses auto-generated filters:
- `name_Icontains` - String
- `price_Gte`, `price_Lte` - Float
- `stock_Gte`, `stock_Lte` - Int
- `createdAt_Gte`, `createdAt_Lte` - DateTime
- Plus pagination: `first`, `last`, `before`, `after`

## Sorting/Ordering:

### For Connection Field (`products`):
The auto-generated Connection fields might support ordering, but it depends on your FilterSet configuration.

### For Manual Fields (`filteredProducts`):
If you want sorting, you'd need to use an advanced filter or add ordering parameters to your resolver.

## Real-World Product Queries:

### Inventory Management:
```graphql
query InventoryCheck {
  # Low stock products in mid-price range
  lowStockProducts: filteredProducts(
    priceGte: 200.0
    priceLte: 800.0
    lowStock: 5
  ) {
    id
    name
    price
    stock
  }
  
  # Out of stock products
  outOfStockProducts: filteredProducts(outOfStock: true) {
    id
    name
    price
  }
}
```

### E-commerce Product Listing:
```graphql
query ProductListing {
  laptops: filteredProducts(
    name: "laptop"
    inStock: true
    priceGte: 500.0
    priceLte: 2000.0
  ) {
    id
    name
    price
    stock
  }
}
```

### Budget Products:
```graphql
query BudgetProducts {
  filteredProducts(priceCategory: "budget") {
    id
    name
    price
    stock
  }
}
```

## Quick Fix for Your Query:

**Change this:**
```graphql
allProducts(filter: { priceGte: 100, priceLte: 1000 }, orderBy: "-stock")
```

**To this:**
```graphql
filteredProducts(priceGte: 100.0, priceLte: 1000.0)
```

**Or for Connection style with edges/node:**
```graphql
products(price_Gte: 100.0, price_Lte: 1000.0, first: 10)
```
