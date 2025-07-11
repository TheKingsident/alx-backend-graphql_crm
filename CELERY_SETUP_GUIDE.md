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
- `debug_task()` - Simple test task

### 4. `alx_backend_graphql/settings.py`
- Added Celery configuration with Redis broker
- Added Celery Beat schedule for periodic tasks
- Configured task serialization and timezone settings

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
from crm.tasks import log_crm_heartbeat_task, update_low_stock_task, debug_task

# Run tasks asynchronously
result1 = log_crm_heartbeat_task.delay()
result2 = update_low_stock_task.delay()
result3 = debug_task.delay()

# Check results
print(result1.get())
print(result2.get())
print(result3.get())
```

### Test from Python Script
```python
from crm.tasks import debug_task

# This will add the task to the queue
result = debug_task.delay()
print(f"Task ID: {result.id}")
print(f"Task Result: {result.get()}")
```

## Scheduled Tasks

The following periodic tasks are configured:

1. **Heartbeat Task**: Runs every 5 minutes
   - Logs CRM system health to `/tmp/crm_heartbeat_log.txt`
   - Checks GraphQL endpoint responsiveness

2. **Low Stock Update**: Runs every 12 hours
   - Updates products with stock < 10
   - Logs results to `/tmp/low_stock_updates_log.txt`

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

## Next Steps

1. **Start Redis**: `redis-server`
2. **Start Celery Worker**: `celery -A crm worker --loglevel=info`
3. **Start Celery Beat**: `celery -A crm beat --loglevel=info`
4. **Test Tasks**: Use Django shell or create test scripts
5. **Monitor**: Install and use Flower for task monitoring

Your Celery setup is now complete and ready for use!
