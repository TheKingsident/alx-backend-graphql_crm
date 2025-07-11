# Celery Setup Guide

## Overview
You've successfully set up Celery with Redis as the message broker for your Django CRM application.

## Files Created/Modified

### 1. `crm/celery.py`
- Initializes the Celery app with Redis broker configuration
- Sets up Redis at `redis://localhost:6379/0`
- Configures JSON serialization and UTC timezone

### 2. `crm/__init__.py`
- Updated to load the Celery app when Django starts
- Ensures shared_task decorators work properly

### 3. `crm/tasks.py`
- Contains Celery task wrappers for your cron functions
- `log_crm_heartbeat_task()` - Celery version of heartbeat logging
- `update_low_stock_task()` - Celery version of low stock updates
- `generate_crm_report()` - Celery version of CRM report generation
- `debug_task()` - Simple test task

### 4. `alx_backend_graphql/settings.py`
- Added Celery configuration with Redis broker
- Added Celery Beat schedule for periodic tasks
- Configured task serialization and timezone settings
- Added crontab import for advanced scheduling

### 5. `crm/schema.py`
- Added `CRMStatsType` for aggregated statistics
- Added `crm_stats` query field to fetch total customers, orders, and revenue
- Added resolver `resolve_crm_stats()` that uses Django ORM aggregation

### 6. `crm/cron.py`
- Added `generate_crm_report()` function
- Uses GraphQL client to query CRM statistics
- Formats timestamp as `YYYY-MM-DD HH:MM:SS`
- Updated `main()` function to include report generation

## Prerequisites

### Install Redis Server
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# macOS
brew install redis

# Start Redis service
sudo systemctl start redis-server
# or
redis-server
```

### Install Python Packages (Already Done)
```bash
pip install celery redis django-celery-beat
```

## Running Celery

### 1. Start Redis Server
```bash
redis-server
```

### 2. Start Celery Worker (in a new terminal)
```bash
cd /home/cakemurderer/ALX_Projects/alx_backend_graphql
source env/bin/activate
celery -A crm worker --loglevel=info
```

### 3. Start Celery Beat (for periodic tasks, in another terminal)
```bash
cd /home/cakemurderer/ALX_Projects/alx_backend_graphql
source env/bin/activate
celery -A crm beat --loglevel=info
```

### 4. Start Django Development Server (in another terminal)
```bash
cd /home/cakemurderer/ALX_Projects/alx_backend_graphql
source env/bin/activate
python manage.py runserver
```

## Testing Celery Tasks

### Test from Django Shell
```python
# Start Django shell
python manage.py shell

# Import and test tasks
from crm.tasks import log_crm_heartbeat_task, update_low_stock_task, generate_crm_report, debug_task

# Run tasks asynchronously
result1 = log_crm_heartbeat_task.delay()
result2 = update_low_stock_task.delay()
result3 = generate_crm_report.delay()
result4 = debug_task.delay()

# Check results
print(result1.get())
print(result2.get())
print(result3.get())
print(result4.get())
```

### Test from Python Script
```python
from crm.tasks import debug_task, generate_crm_report

# This will add the task to the queue
result1 = debug_task.delay()
result2 = generate_crm_report.delay()

print(f"Debug Task ID: {result1.id}")
print(f"Debug Task Result: {result1.get()}")

print(f"Report Task ID: {result2.id}")
print(f"Report Task Result: {result2.get()}")
```

## Testing the CRM Report Feature

### Test CRM Stats GraphQL Query
```bash
# Using curl
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query": "{ crmStats { totalCustomers totalOrders totalRevenue } }"}'
```

### Test CRM Report Generation
```python
# From Django shell
python manage.py shell

# Test the cron function directly
from crm.cron import generate_crm_report
generate_crm_report()

# Check the log output
import subprocess
subprocess.run(['cat', '/tmp/crm_report_log.txt'])
```

### Test Celery Task
```python
# From Django shell
from crm.tasks import generate_crm_report
result = generate_crm_report.delay()
print(result.get())
```

## Scheduled Tasks

The following periodic tasks are configured:

1. **Heartbeat Task**: Runs every 5 minutes
   - Logs CRM system health to `/tmp/crm_heartbeat_log.txt`
   - Checks GraphQL endpoint responsiveness

2. **Low Stock Update**: Runs every 12 hours
   - Updates products with stock < 10
   - Logs results to `/tmp/low_stock_updates_log.txt`

3. **CRM Report Generation**: Runs every Monday at 6:00 AM
   - Generates comprehensive CRM statistics report
   - Fetches total customers, orders, and revenue via GraphQL
   - Logs results to `/tmp/crm_report_log.txt`
   - Uses format: `YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue`

## Monitoring

### Celery Flower (Web-based monitoring)
```bash
pip install flower
celery -A crm flower
# Visit http://localhost:5555 for web interface
```

### Check Task Status
```bash
# List active tasks
celery -A crm inspect active

# List scheduled tasks
celery -A crm inspect scheduled

# List registered tasks
celery -A crm inspect registered
```

## Configuration Summary

- **Broker**: Redis (`redis://localhost:6379/0`)
- **Result Backend**: Redis (`redis://localhost:6379/0`)
- **Serialization**: JSON
- **Timezone**: UTC
- **Task Discovery**: Automatic from all Django apps
- **Scheduled Tasks**: 3 periodic tasks (heartbeat, low stock update, CRM report)
- **GraphQL Integration**: CRM stats query with aggregated data

## Next Steps

1. **Start Redis**: `redis-server`
2. **Start Celery Worker**: `celery -A crm worker --loglevel=info`
3. **Start Celery Beat**: `celery -A crm beat --loglevel=info`
4. **Test Tasks**: Use Django shell or create test scripts
5. **Monitor**: Install and use Flower for task monitoring

Your Celery setup is now complete and ready for use!
