# GraphQL Customer Filter Examples

This file contains examples of how to use the CustomerFilter in GraphQL queries.

## Basic Filter Usage

### 1. Filter by Name (Case-insensitive partial match)

```graphql
query {
  filteredCustomers(name: "john") {
    id
    name
    email
    phone
    createdAt
  }
}
```

This will return all customers whose name contains "john" (case-insensitive).
Examples: "John Doe", "Johnny Smith", "Johnson", etc.

### 2. Filter by Email (Case-insensitive partial match)

```graphql
query {
  filteredCustomers(email: "gmail") {
    id
    name
    email
    phone
    createdAt
  }
}
```

This will return all customers whose email contains "gmail".
Examples: "user@gmail.com", "test.Gmail@example.com", etc.

### 3. Date Range Filtering

#### Filter customers created after a specific date:
```graphql
query {
  filteredCustomers(createdAtGte: "2024-01-01T00:00:00Z") {
    id
    name
    email
    createdAt
  }
}
```

#### Filter customers created before a specific date:
```graphql
query {
  filteredCustomers(createdAtLte: "2024-12-31T23:59:59Z") {
    id
    name
    email
    createdAt
  }
}
```

#### Filter customers created within a date range:
```graphql
query {
  filteredCustomers(
    createdAtGte: "2024-01-01T00:00:00Z"
    createdAtLte: "2024-12-31T23:59:59Z"
  ) {
    id
    name
    email
    createdAt
  }
}
```

### 4. Custom Phone Pattern Filter (Challenge)

#### Find customers with US phone numbers (starting with +1):
```graphql
query {
  filteredCustomers(phonePattern: "+1") {
    id
    name
    email
    phone
  }
}
```

#### Find customers with UK phone numbers:
```graphql
query {
  filteredCustomers(phonePattern: "+44") {
    id
    name
    email
    phone
  }
}
```

#### Search for specific area code (e.g., 555):
```graphql
query {
  filteredCustomers(phonePattern: "555") {
    id
    name
    email
    phone
  }
}
```

#### Search for US numbers using keyword:
```graphql
query {
  filteredCustomers(phonePattern: "us") {
    id
    name
    email
    phone
  }
}
```

## Advanced Filter Usage

### 5. Combining Multiple Filters

```graphql
query {
  filteredCustomers(
    name: "john"
    email: "gmail"
    phonePattern: "+1"
    createdAtGte: "2024-01-01T00:00:00Z"
  ) {
    id
    name
    email
    phone
    createdAt
  }
}
```

This query finds customers who:
- Have "john" in their name
- Have "gmail" in their email
- Have a US phone number (+1)
- Were created after January 1, 2024

### 6. Email Domain Filtering

```graphql
query {
  filteredCustomers(emailDomain: "gmail.com") {
    id
    name
    email
  }
}
```

### 7. Filter by Phone Availability

#### Customers with phone numbers:
```graphql
query {
  filteredCustomers(hasPhone: true) {
    id
    name
    email
    phone
  }
}
```

#### Customers without phone numbers:
```graphql
query {
  filteredCustomers(hasPhone: false) {
    id
    name
    email
    phone
  }
}
```

### 8. Pagination

```graphql
query {
  filteredCustomers(
    name: "john"
    limit: 10
    offset: 0
  ) {
    id
    name
    email
    phone
  }
}
```

### 9. Advanced Filtering with Ordering

```graphql
query {
  advancedFilteredCustomers(
    name: "john"
    ordering: "-createdAt"  # Order by creation date, newest first
    limit: 5
  ) {
    id
    name
    email
    phone
    createdAt
  }
}
```

Available ordering options:
- `"name"` - Order by name (ascending)
- `"-name"` - Order by name (descending) 
- `"email"` - Order by email (ascending)
- `"-email"` - Order by email (descending)
- `"createdAt"` - Order by creation date (ascending)
- `"-createdAt"` - Order by creation date (descending)
- `"updatedAt"` - Order by update date (ascending)
- `"-updatedAt"` - Order by update date (descending)

### 10. Using DjangoFilterConnectionField (Relay-style)

```graphql
query {
  customers(
    name_Icontains: "john"
    email_Icontains: "gmail"
    phonePattern: "+1"
    first: 10
  ) {
    edges {
      node {
        id
        name
        email
        phone
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

## Real-World Usage Examples

### Example 1: Customer Support Dashboard
Find all customers with Gmail addresses who registered in the last month:

```graphql
query {
  filteredCustomers(
    emailDomain: "gmail.com"
    createdAtGte: "2024-06-01T00:00:00Z"
    ordering: "-createdAt"
  ) {
    id
    name
    email
    phone
    createdAt
  }
}
```

### Example 2: Marketing Campaign
Find US customers (phone starts with +1) for SMS marketing:

```graphql
query {
  filteredCustomers(
    phonePattern: "+1"
    hasPhone: true
  ) {
    id
    name
    phone
    email
  }
}
```

### Example 3: Customer Search
Search for a specific customer by partial name or email:

```graphql
query {
  filteredCustomers(name: "smith") {
    id
    name
    email
    phone
  }
}
```

OR

```graphql
query {
  filteredCustomers(email: "john.smith") {
    id
    name
    email
    phone
  }
}
```

### Example 4: Analytics Query  
Get customers from different time periods for analysis:

```graphql
query {
  q1Customers: filteredCustomers(
    createdAtGte: "2024-01-01T00:00:00Z"
    createdAtLte: "2024-03-31T23:59:59Z"
  ) {
    id
    name
    createdAt
  }
  
  q2Customers: filteredCustomers(
    createdAtGte: "2024-04-01T00:00:00Z"
    createdAtLte: "2024-06-30T23:59:59Z"
  ) {
    id
    name
    createdAt
  }
}
```

## Testing Your Filters

You can test these queries using:
1. GraphQL Playground (if enabled)
2. GraphiQL interface
3. Postman with GraphQL support
4. Your frontend application

### Testing with curl:

```bash
curl -X POST \
  http://localhost:8000/graphql/ \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "query { filteredCustomers(name: \"john\") { id name email phone } }"
  }'
```
