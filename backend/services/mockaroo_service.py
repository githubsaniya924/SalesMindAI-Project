import requests
import os

def fetch_mockaroo_leads():
    api_key = os.getenv("MOCKAROO_API_KEY")
    # FIX: Use the api_key variable and ensure the URL endpoint is correct
    url = f"https://my.api.mockaroo.com/b2c_leads.json?key=47d7caa0"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        # This helps you debug if the key is expired or wrong
        print(f"Mockaroo Error: {response.status_code} - {response.text}")
        return []
    except Exception as e:
        print(f"Request failed: {e}")
        return []