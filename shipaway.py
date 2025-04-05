import requests
import json

url = "https://shipaway.io/api/v1/usps/create"

def create_label(data):
    """
    Create a shipping label using the Shipaway API
    
    Args:
        data (dict): Label data with sender, recipient, and package information
        
    Returns:
        tuple: (success, response) where success is a boolean and response is the API response
    """
    try:
        headers = {
            'Authorization': data["uuid"],
            'Content-Type': 'application/json'
        }
        
        payload = json.dumps(data)
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


