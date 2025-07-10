# Customer Cleanup Cron Job

This directory contains scripts for automatically cleaning up inactive customers.

## Files

### clean_inactive_customers.sh
A shell script that:
- Deletes customers who have no orders in the past year
- Logs the operation results to `/tmp/customer_cleanup_log.txt`
- Includes timestamp and count of deleted customers

### customer_cleanup_crontab.txt
Contains the crontab entry to run the cleanup script every Sunday at 2:00 AM.

## Setup Instructions

1. **Make sure the script is executable** (already done):
   ```bash
   chmod +x /path/to/crm/cron_jobs/clean_inactive_customers.sh
   ```

2. **Add the cron job to your crontab**:
   ```bash
   crontab -e
   ```
   Then add the line from `customer_cleanup_crontab.txt`:
   ```
   0 2 * * 0 /home/cakemurderer/ALX_Projects/alx_backend_graphql/crm/cron_jobs/clean_inactive_customers.sh
   ```

3. **Alternative: Load the crontab directly**:
   ```bash
   crontab crm/cron_jobs/customer_cleanup_crontab.txt
   ```

## Manual Testing

You can test the script manually:
```bash
./crm/cron_jobs/clean_inactive_customers.sh
```

Check the log file:
```bash
cat /tmp/customer_cleanup_log.txt
```

## Cron Schedule Explanation

`0 2 * * 0` means:
- `0` - At minute 0
- `2` - At hour 2 (2:00 AM)
- `*` - Every day of month
- `*` - Every month
- `0` - On Sunday (0 = Sunday, 1 = Monday, etc.)

So the script runs every Sunday at 2:00 AM.

## What the Script Does

1. **Identifies inactive customers**: Customers with no orders OR customers whose most recent order is older than 1 year
2. **Deletes them**: Uses Django ORM to safely delete the records
3. **Logs the operation**: Records timestamp and number of deleted customers
4. **Error handling**: Logs any errors that occur during the process

## Log File Format

The log file (`/tmp/customer_cleanup_log.txt`) contains entries like:
```
[2024-01-14 02:00:01] Starting customer cleanup...
[2024-01-14 02:00:02] Successfully deleted 15 inactive customers
[2024-01-14 02:00:02] Customer cleanup completed

[2024-01-21 02:00:01] Starting customer cleanup...
[2024-01-21 02:00:02] Successfully deleted 0 inactive customers
[2024-01-21 02:00:02] Customer cleanup completed
```
