# CRM Database Seeding

This directory contains scripts to populate your CRM database with sample data for testing GraphQL mutations and queries.

## Available Seeding Methods

### Method 1: Direct Python Script

Run the standalone seed script:

```bash
cd /home/cakemurderer/ALX_Projects/alx_backend_graphql
python seed.py
```

This will create:
- 10 sample customers
- 15 sample products  
- 20 sample orders

### Method 2: Django Management Command

Use Django's management command system:

```bash
cd /home/cakemurderer/ALX_Projects/alx_backend_graphql
python manage.py seed_db
```

#### Management Command Options

```bash
# Clear existing data before seeding
python manage.py seed_db --clear

# Customize the number of records
python manage.py seed_db --customers 20 --products 30 --orders 50

# Clear data and create custom amounts
python manage.py seed_db --clear --customers 15 --products 25 --orders 40
```

## Before Running the Seed Scripts

1. **Make sure your database is set up:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Ensure your Django server can run:**
   ```bash
   python manage.py runserver
   ```

## Sample Data Created

### Customers
- Names: Alice Johnson, Bob Smith, Carol Williams, etc.
- Valid email addresses and phone numbers
- Phone numbers in different formats (+1234567890, 123-456-7890)

### Products
- Tech products: MacBook Pro, iPhone, iPad, etc.
- Realistic prices from $24.99 to $2499.99
- Stock quantities between 5-200 items

### Orders
- Random customer-product associations
- 1-4 products per order
- Order dates spread over the last 30 days
- Calculated total amounts

## Testing GraphQL Mutations

After seeding, you can test these mutations at `http://localhost:8000/graphql/`:

### Create a Customer
```graphql
mutation {
  createCustomer(input: {
    name: "Test User"
    email: "test@example.com"
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
      phone
    }
    message
    errors {
      field
      message
    }
  }
}
```

### Create a Product
```graphql
mutation {
  createProduct(input: {
    name: "Test Product"
    price: 99.99
    stock: 10
  }) {
    product {
      id
      name
      price
      stock
    }
    errors {
      field
      message
    }
  }
}
```

### Create an Order
```graphql
mutation {
  createOrder(input: {
    customerId: "CUSTOMER_ID_HERE"
    productIds: ["PRODUCT_ID_1", "PRODUCT_ID_2"]
  }) {
    order {
      id
      customer {
        name
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
    errors {
      field
      message
    }
  }
}
```

### Query Sample Data
```graphql
query {
  allCustomers {
    id
    name
    email
    phone
  }
  
  allProducts {
    id
    name
    price
    stock
  }
  
  allOrders {
    id
    customer {
      name
    }
    products {
      name
      price
    }
    totalAmount
    orderDate
  }
}
```

## Troubleshooting

If you encounter errors:

1. **Import errors**: Make sure you're running from the project root directory
2. **Database errors**: Ensure migrations are applied (`python manage.py migrate`)
3. **Permission errors**: Check file permissions on the seed.py script
4. **GraphQL errors**: Verify the server is running and accessible at the GraphQL endpoint

## Clearing Data

To clear all seeded data:

```bash
# Using management command
python manage.py seed_db --clear

# Or manually in Django shell
python manage.py shell
>>> from crm.models import Customer, Product, Order
>>> Order.objects.all().delete()
>>> Product.objects.all().delete()  
>>> Customer.objects.all().delete()
```
