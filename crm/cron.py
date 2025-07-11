from datetime import datetime
import requests
import json

def log_crm_heartbeat():
    """Log a heartbeat to confirm CRM application's health"""
    LOG_FILE = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    heartbeat_message = f"{timestamp} CRM is alive"
    
    # Optionally, query the GraphQL hello field to verify endpoint responsiveness
    try:
        # GraphQL hello query
        query = {
            "query": "{ hello }"
        }
        
        # Get CSRF token first
        session = requests.Session()
        get_response = session.get("http://localhost:8000/graphql/")
        csrf_token = session.cookies.get('csrftoken')
        
        # Headers for the GraphQL request
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Referer': 'http://localhost:8000/graphql/',
        }
        
        # Make the GraphQL request
        response = session.post(
            "http://localhost:8000/graphql/",
            json=query,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result and 'hello' in result['data']:
                heartbeat_message += f" - GraphQL endpoint responsive: {result['data']['hello']}"
            else:
                heartbeat_message += " - GraphQL endpoint reachable but no hello field"
        else:
            heartbeat_message += f" - GraphQL endpoint error: HTTP {response.status_code}"
            
    except Exception as e:
        heartbeat_message += f" - GraphQL check failed: {str(e)}"
    
    # Append to the log file
    with open(LOG_FILE, "a") as f:
        f.write(f"{heartbeat_message}\n")