# Correct GraphQL Query Examples for CustomerFilter

## Issue with Your Query:
Your query was using `allCustomers` with a `filter` argument, but that field doesn't accept filters.

### ❌ Wrong Query (what you tried):
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

## ✅ Correct Query Options:

### Option 1: Using `filteredCustomers` (Manual Filter Arguments)
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
      startCursor
      endCursor
    }
  }
}
```

### Option 3: More Complete Filter Examples

#### Filter by name and email domain:
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
    createdAt
  }
}
```

#### Filter with phone pattern and date range:
```graphql
query {
  filteredCustomers(
    name: "Ali"
    createdAtGte: "2025-01-01T00:00:00Z"
    createdAtLte: "2025-12-31T23:59:59Z"
    phonePattern: "+1"
  ) {
    id
    name
    email
    phone
    createdAt
  }
}
```

#### Advanced filtering with ordering:
```graphql
query {
  advancedFilteredCustomers(
    name: "Ali"
    createdAtGte: "2025-01-01T00:00:00Z"
    ordering: "-createdAt"
    limit: 5
  ) {
    id
    name
    email
    createdAt
  }
}
```

## Available Filter Fields for Customers:

### Basic Filters:
- `name` - Case-insensitive partial match
- `email` - Case-insensitive partial match
- `createdAtGte` - Created on or after date
- `createdAtLte` - Created on or before date
- `phonePattern` - Custom phone pattern matching
- `emailDomain` - Filter by email domain
- `hasPhone` - Boolean filter for phone availability

### Advanced Filters (in `advancedFilteredCustomers`):
- All basic filters plus:
- `ordering` - Sort results (e.g., "name", "-createdAt")
- `limit` - Limit number of results
- `offset` - Pagination offset

## Why Your Original Query Failed:

1. **`allCustomers` field**: This is a simple list field that returns all customers without any filtering capability
2. **`filter` argument**: This argument doesn't exist on the `allCustomers` field
3. **`edges/node` structure**: This is only available on Connection fields (like our `customers` field), not on simple List fields

## Query Field Reference:

| Field Name | Type | Supports Filters | Supports Pagination | Structure |
|------------|------|------------------|-------------------|-----------|
| `allCustomers` | List | ❌ No | ❌ No | Simple array |
| `filteredCustomers` | List | ✅ Yes (manual args) | ✅ Yes (limit/offset) | Simple array |
| `advancedFilteredCustomers` | List | ✅ Yes (manual args) | ✅ Yes (limit/offset) | Simple array |
| `customers` | Connection | ✅ Yes (auto-generated) | ✅ Yes (Relay-style) | edges/node |

## Test Your Filters:

You can test these queries in GraphQL Playground or any GraphQL client. Make sure your Django server is running and navigate to your GraphQL endpoint (usually `http://localhost:8000/graphql/`).
