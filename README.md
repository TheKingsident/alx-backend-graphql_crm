# Django GraphQL CRM System

A comprehensive Customer Relationship Management (CRM) system built with Django, GraphQL, and Celery. This project demonstrates advanced filtering, mutations, background task processing, and automated reporting capabilities.

## 🚀 Features

### Core CRM Functionality
- **Customer Management**: Create, read, update customers with validation
- **Product Management**: Manage products with stock tracking
- **Order Management**: Process orders with customer-product relationships
- **Advanced Filtering**: Filter customers, products, and orders by multiple criteria

### GraphQL API
- **Queries**: Comprehensive filtering with django-filter integration
- **Mutations**: Create customers, products, orders, and bulk operations
- **Health Check**: System status monitoring via GraphQL
- **Analytics**: CRM statistics (total customers, orders, revenue)

### Background Tasks & Automation
- **Celery Integration**: Redis-backed task queue
- **Automated Reports**: Weekly CRM statistics generation
- **Stock Management**: Automatic low-stock product restocking
- **Health Monitoring**: System heartbeat logging
- **Cron Jobs**: Scheduled maintenance and cleanup tasks

### Advanced Features
- **Bulk Operations**: Create multiple customers in a single request
- **Custom Validators**: Phone number and email validation
- **Error Handling**: Comprehensive error reporting
- **Logging**: Detailed activity and error logs
- **UUID Primary Keys**: Enhanced security and scalability

## 🛠️ Technology Stack

- **Backend**: Django 5.1
- **API**: GraphQL (Graphene Django)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Task Queue**: Celery with Redis broker
- **Filtering**: django-filter
- **Scheduling**: django-crontab + Celery Beat
- **Validation**: Django validators + custom validation

## 📋 Prerequisites

- Python 3.8+
- Redis server
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd alx_backend_graphql
```

### 2. Set Up Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- Django 5.1
- graphene-django
- django-filter
- celery
- redis
- django-celery-beat
- django-crontab

### 4. Set Up Database
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Install and Start Redis
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install redis-server
redis-server

# macOS
brew install redis
brew services start redis

# Windows (using Docker)
docker run -d -p 6379:6379 redis:latest
```

## 🚀 Running the Application

### 1. Start Django Development Server
```bash
python manage.py runserver
```

### 2. Start Celery Worker (New Terminal)
```bash
celery -A crm worker --loglevel=info
```

### 3. Start Celery Beat Scheduler (New Terminal)
```bash
celery -A crm beat --loglevel=info
```

### 4. Access the Application
- **GraphQL Playground**: http://localhost:8000/graphql/
- **Django Admin**: http://localhost:8000/admin/

## 📖 API Documentation

### GraphQL Endpoints

#### Health Check
```graphql
query {
  hello
}
```

#### CRM Statistics
```graphql
query {
  crmStats {
    totalCustomers
    totalOrders
    totalRevenue
  }
}
```

#### Customer Operations
```graphql
# Get all customers
query {
  allCustomers {
    id
    name
    email
    phone
    createdAt
  }
}

# Create customer
mutation {
  createCustomer(input: {
    name: "John Doe"
    email: "john@example.com"
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
    }
    errors {
      field
      message
    }
  }
}

# Bulk create customers
mutation {
  bulkCreateCustomers(input: [
    {name: "Alice", email: "alice@example.com"}
    {name: "Bob", email: "bob@example.com"}
  ]) {
    customers {
      id
      name
      email
    }
    errors {
      field
      message
    }
  }
}
```

#### Advanced Filtering
```graphql
# Filter customers
query {
  filteredCustomers(
    name: "John"
    emailDomain: "gmail.com"
    hasPhone: true
    createdAtGte: "2024-01-01"
    limit: 10
  ) {
    id
    name
    email
    phone
  }
}

# Filter products
query {
  filteredProducts(
    priceGte: 10.0
    priceLte: 100.0
    lowStock: 10
    inStock: true
  ) {
    id
    name
    price
    stock
  }
}

# Filter orders
query {
  filteredOrders(
    totalAmountGte: 100.0
    customerName: "John"
    recentOrders: true
    highValueOrders: true
  ) {
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

#### Product Operations
```graphql
# Create product
mutation {
  createProduct(input: {
    name: "Laptop"
    price: 999.99
    stock: 50
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

# Update low stock products
mutation {
  updateLowStockProducts {
    updatedProducts {
      name
      stock
    }
    successMessage
    count
  }
}
```

#### Order Operations
```graphql
# Create order
mutation {
  createOrder(input: {
    customerId: "customer-uuid"
    productIds: ["product-uuid-1", "product-uuid-2"]
    totalAmount: 150.00
  }) {
    order {
      id
      totalAmount
      orderDate
      customer {
        name
      }
      products {
        name
        price
      }
    }
    errors {
      field
      message
    }
  }
}
```

## 🤖 Background Tasks

### Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| Heartbeat | Every 5 minutes | System health check and GraphQL endpoint monitoring |
| Low Stock Update | Every 12 hours | Automatically restock products with stock < 10 |
| CRM Report | Monday 6:00 AM | Generate weekly statistics report |

### Manual Task Execution
```python
# Django shell
python manage.py shell

from crm.tasks import log_crm_heartbeat_task, update_low_stock_task, generate_crm_report

# Execute tasks
result1 = log_crm_heartbeat_task.delay()
result2 = update_low_stock_task.delay()
result3 = generate_crm_report.delay()

# Check results
print(result1.get())
print(result2.get())
print(result3.get())
```

## 📊 Data Seeding

### Seed the Database
```bash
# Run the seeding script
python seed.py

# Or use Django management command
python manage.py seed_db
```

This will create sample:
- 10 customers with realistic data
- 15 products with varying prices and stock levels
- 25 orders with random customer-product combinations

## 📁 Project Structure

```
alx_backend_graphql/
├── alx_backend_graphql/          # Main Django project
│   ├── __init__.py
│   ├── settings.py               # Django settings with Celery config
│   ├── urls.py                   # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── crm/                          # CRM Django app
│   ├── models.py                 # Customer, Product, Order models
│   ├── schema.py                 # GraphQL schema and resolvers
│   ├── filters.py                # Advanced filtering classes
│   ├── tasks.py                  # Celery task definitions
│   ├── celery.py                 # Celery app configuration
│   ├── cron.py                   # Cron job functions
│   ├── admin.py                  # Django admin configuration
│   ├── migrations/               # Database migrations
│   ├── management/
│   │   └── commands/
│   │       └── seed_db.py        # Custom management command
│   └── cron_jobs/                # Shell scripts for cron
│       ├── clean_inactive_customers.sh
│       └── send_order_reminders.py
├── env/                          # Virtual environment
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
├── seed.py                       # Database seeding script
├── CELERY_SETUP_GUIDE.md        # Celery setup documentation
└── README.md                     # This file
```

## 🧪 Testing

### Test GraphQL Queries
```bash
# Using curl
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ hello }"}'

curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ crmStats { totalCustomers totalOrders totalRevenue } }"}'
```

### Test Celery Tasks
```python
# Test from Python script
from crm.tasks import debug_task
result = debug_task.delay()
print(f"Task ID: {result.id}")
print(f"Result: {result.get()}")
```

### Test Cron Functions
```python
# Test cron functions directly
from crm.cron import log_crm_heartbeat, update_low_stock, generate_crm_report

log_crm_heartbeat()
update_low_stock()
generate_crm_report()

# Check log files
import subprocess
subprocess.run(['cat', '/tmp/crm_heartbeat_log.txt'])
subprocess.run(['cat', '/tmp/low_stock_updates_log.txt'])
subprocess.run(['cat', '/tmp/crm_report_log.txt'])
```

## 📝 Logging

The application generates logs in `/tmp/`:
- `/tmp/crm_heartbeat_log.txt` - System health checks
- `/tmp/low_stock_updates_log.txt` - Stock update operations
- `/tmp/crm_report_log.txt` - Weekly CRM reports

## 🔒 Security Features

- UUID primary keys for enhanced security
- Email uniqueness validation
- Phone number format validation
- CSRF protection for GraphQL mutations
- Input sanitization and validation

## 🚀 Production Deployment

### Environment Variables
```bash
# .env file
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=yourdomain.com
```

### Database Migration
```bash
# For PostgreSQL
pip install psycopg2-binary
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

### Process Management
Use a process manager like Supervisor or systemd to manage:
- Django application server (Gunicorn)
- Celery worker processes
- Celery beat scheduler
- Redis server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Redis Connection Error**
```bash
# Start Redis server
redis-server
# Or check if running
redis-cli ping
```

**Celery Worker Not Starting**
```bash
# Check Redis connection
redis-cli ping
# Restart Celery worker
celery -A crm worker --loglevel=info
```

**GraphQL Schema Errors**
```bash
# Check for migration issues
python manage.py makemigrations
python manage.py migrate
```

**Import Errors**
```bash
# Ensure virtual environment is activated
source env/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the CELERY_SETUP_GUIDE.md for detailed Celery configuration
- Review the logs in `/tmp/` for debugging information

## 🎯 Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Advanced analytics and reporting dashboard
- [ ] Email notification system
- [ ] API rate limiting and authentication
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests
- [ ] Automated testing suite
- [ ] Performance monitoring and metrics
