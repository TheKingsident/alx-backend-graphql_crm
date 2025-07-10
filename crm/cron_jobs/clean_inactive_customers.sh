#!/bin/bash

# Shell script to clean up inactive customers (customers with no orders in the past year)
# This script uses Django's manage.py shell to execute the cleanup operation

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the Django project root (two levels up from crm/cron_jobs)
# cwd
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Log file path
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Timestamp for logging
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Change to project directory
cd "$PROJECT_ROOT" || exit 1

# Activate virtual environment if it exists
if [ -f "env/bin/activate" ]; then
    source env/bin/activate
fi

# Python command to delete inactive customers
PYTHON_COMMAND="
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
from django.db.models import Q, Max

# Calculate the date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# First, find all customer IDs that have recent orders (within the past year)
recent_customer_ids = Customer.objects.filter(
    orders__order_date__gte=one_year_ago
).values_list('id', flat=True).distinct()

# Find customers who are NOT in the recent customers list (inactive customers)
inactive_customers = Customer.objects.exclude(id__in=recent_customer_ids)

# Count the customers before deletion
count = inactive_customers.count()

# Delete the inactive customers
if count > 0:
    deleted_count, _ = inactive_customers.delete()
    print(f'Deleted {deleted_count} inactive customers')
    print(deleted_count)
else:
    print('No inactive customers found')
    print(0)
"

# Execute the Django shell command and capture the output
echo "[$TIMESTAMP] Starting customer cleanup..." >> "$LOG_FILE"

# Run the Django shell command and capture the result
RESULT=$(python manage.py shell -c "$PYTHON_COMMAND" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    # Extract the number from the last line of output
    DELETED_COUNT=$(echo "$RESULT" | tail -n 1)
    echo "[$TIMESTAMP] Successfully deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] Error during cleanup: $RESULT" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] Customer cleanup completed" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"