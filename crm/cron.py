from datetime import datetime
import requests
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Log a heartbeat to confirm CRM application's health"""
    LOG_FILE = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    heartbeat_message = f"{timestamp} CRM is alive"
    
    # Optionally, query the GraphQL hello field to verify endpoint responsiveness
    try:
        # Setup GraphQL client with CSRF handling
        session = requests.Session()
        get_response = session.get("http://localhost:8000/graphql/")
        csrf_token = session.cookies.get('csrftoken')
        
        headers = {
            'X-CSRFToken': csrf_token,
            'Referer': 'http://localhost:8000/graphql/',
        }
        
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            use_json=True,
            headers=headers,
            cookies=session.cookies
        )
        
        client = Client(transport=transport, fetch_schema_from_transport=False)
        
        # GraphQL hello query using gql to check endpoint health
        query = gql("{ hello }")
        
        # Execute the query
        result = client.execute(query)
        
        if result and 'hello' in result:
            heartbeat_message += f" - GraphQL endpoint responsive: {result['hello']}"
        else:
            heartbeat_message += " - GraphQL endpoint reachable but no hello response"
            
    except Exception as e:
        heartbeat_message += f" - GraphQL check failed: {str(e)}"
    
    # Append to the log file
    with open(LOG_FILE, "a") as f:
        f.write(f"{heartbeat_message}\n")