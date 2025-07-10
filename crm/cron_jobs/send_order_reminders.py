#!/usr/bin/env python3
"""
Order Reminders Script

This script uses the gql library to query the GraphQL endpoint for orders placed 
within the last 7 days and logs each order's ID and customer email for reminder purposes.
"""

import os
import sys
import django
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests

# Add the project root to Python path and setup Django
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.append(project_root)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

def setup_graphql_client():
    """Setup and return a GraphQL client with CSRF handling."""
    # Create a session to handle cookies and CSRF
    session = requests.Session()
    
    # Get CSRF token by making a GET request first
    get_response = session.get("http://localhost:8000/graphql/")
    csrf_token = session.cookies.get('csrftoken')
    
    # Setup headers with CSRF token
    headers = {
        'X-CSRFToken': csrf_token,
        'Referer': 'http://localhost:8000/graphql/',
    }
    
    # Create transport with the headers and use the session's cookies
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        use_json=True,
        headers=headers,
        cookies=session.cookies
    )
    
    return Client(transport=transport, fetch_schema_from_transport=False)

def get_recent_orders():
    """Query GraphQL for orders placed within the last 7 days."""
    # Calculate date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)
    seven_days_ago_iso = seven_days_ago.isoformat()
    
    # GraphQL query for recent orders
    query = gql("""
        query GetRecentOrders($orderDateGte: DateTime!) {
            filteredOrders(orderDateGte: $orderDateGte) {
                id
                orderDate
                totalAmount
                customer {
                    id
                    name
                    email
                }
            }
        }
    """)
    
    # Execute the query
    client = setup_graphql_client()
    result = client.execute(query, variable_values={
        "orderDateGte": seven_days_ago_iso
    })
    
    return result['filteredOrders']

def log_order_reminder(order_id, customer_email, log_file):
    """Log an order reminder with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] Order ID: {order_id}, Customer Email: {customer_email}\n"
    
    with open(log_file, 'a') as f:
        f.write(log_entry)

def main():
    """Main function to process order reminders."""
    log_file = "/tmp/order_reminders_log.txt"
    
    try:
        # Add starting log entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file, 'a') as f:
            f.write(f"\n[{timestamp}] Starting order reminders processing...\n")
        
        # Get recent orders from GraphQL
        orders = get_recent_orders()
        
        if not orders:
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] No orders found in the last 7 days.\n")
        else:
            # Log each order
            for order in orders:
                log_order_reminder(
                    order['id'], 
                    order['customer']['email'], 
                    log_file
                )
        
        # Add completion log entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] Order reminders processed! Total orders: {len(orders)}\n")
        
        # Print to console
        print("Order reminders processed!")
        
    except Exception as e:
        # Log any errors
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] Error processing order reminders: {str(e)}\n")
        
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
