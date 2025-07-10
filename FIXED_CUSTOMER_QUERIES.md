# CORRECT GraphQL Queries for Your Schema

Based on your actual schema, here are the **correct** ways to filter customers:

## Available Customer Query Fields:

1. `allCustomers` - Simple list, NO filtering ❌
2. `customers` - Connection field with auto-generated filters ✅  
3. `filteredCustomers` - List with manual filter arguments ✅
4. `advancedFilteredCustomers` - List with advanced filters ✅

## ✅ CORRECT Queries for Your Use Case:

### Option 1: Using `filteredCustomers` (Recommended)
```graphql
query {
  filteredCustomers(
    name: "Ali"
    createdAtGte: "2025-01-01T00:00:00Z"
  ) {
    id
    name
    email
    createdAt
  }
}
```

### Option 2: Using `customers` (DjangoFilterConnectionField - Relay Style)
```graphql
query {
  customers(
    name_Icontains: "Ali"
    createdAt_Gte: "2025-01-01T00:00:00Z"
    first: 10
  ) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
  }
}
```

### Option 3: Using `advancedFilteredCustomers` (With Ordering)
```graphql
query {
  advancedFilteredCustomers(
    name: "Ali"
    createdAtGte: "2025-01-01T00:00:00Z"
    ordering: "-createdAt"
    limit: 10
  ) {
    id
    name
    email
    createdAt
  }
}
```

## Why Your Query Failed:

### ❌ Your Original Query:
```graphql
query {
  allCustomers(filter: { nameIcontains: "Ali", createdAtGte: "2025-01-01" }) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

### Problems:
1. **`allCustomers`** - This field doesn't accept any arguments (it's just a simple list)
2. **`filter` argument** - This doesn't exist on any of your fields
3. **`edges/node` structure** - Only works with Connection fields like `customers`

## Complete Filter Examples:

### 1. Filter by Name and Email Domain
```graphql
query {
  filteredCustomers(
    name: "Ali"
    emailDomain: "gmail.com"
  ) {
    id
    name
    email
    phone
  }
}
```

### 2. Filter by Phone Pattern and Date Range
```graphql
query {
  filteredCustomers(
    phonePattern: "+1"
    createdAtGte: "2025-01-01T00:00:00Z"
    createdAtLte: "2025-12-31T23:59:59Z"
  ) {
    id
    name
    email
    phone
    createdAt
  }
}
```

### 3. Filter Customers with Phone Numbers
```graphql
query {
  filteredCustomers(
    hasPhone: true
    name: "Ali"
  ) {
    id
    name
    email
    phone
  }
}
```

### 4. Using Pagination
```graphql
query {
  filteredCustomers(
    name: "Ali"
    limit: 5
    offset: 0
  ) {
    id
    name
    email
    createdAt
  }
}
```

### 5. Advanced Filtering with Ordering
```graphql
query {
  advancedFilteredCustomers(
    name: "Ali"
    createdAtGte: "2025-01-01T00:00:00Z"
    ordering: "-createdAt"  # Newest first
    limit: 10
  ) {
    id
    name
    email
    createdAt
  }
}
```

## Available Filter Arguments for `filteredCustomers`:

- `name` - String (case-insensitive partial match)
- `email` - String (case-insensitive partial match)  
- `createdAtGte` - DateTime (created on or after)
- `createdAtLte` - DateTime (created on or before)
- `phonePattern` - String (custom phone pattern matching)
- `emailDomain` - String (filter by email domain)
- `hasPhone` - Boolean (has phone number or not)
- `limit` - Int (pagination)
- `offset` - Int (pagination)

## Available Filter Arguments for `customers` (Connection):

The `customers` field uses auto-generated filters from DjangoFilterConnectionField:
- `name_Icontains` - String
- `email_Icontains` - String
- `createdAt_Gte` - DateTime
- `createdAt_Lte` - DateTime
- `phone_Exact` - String
- `phone_Icontains` - String
- Plus pagination: `first`, `last`, `before`, `after`

## Test These Queries:

You can test any of these queries in your GraphQL interface. The most straightforward option is **`filteredCustomers`** which matches exactly what you were trying to do!
