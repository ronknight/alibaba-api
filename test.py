import requests
import os
import hashlib
from datetime import datetime
import urllib.parse

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Retrieve variables from environment
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Taobao API endpoint
SECURE_REST_API_ENDPOINT = 'https://eco.taobao.com/router/rest'

def generate_sign(params):
    # Generate MD5 sign
    param_string = ''.join([k + str(params[k]) for k in sorted(params.keys())])
    sign = hashlib.md5((APP_SECRET + param_string + APP_SECRET).encode('utf-8')).hexdigest().upper()
    return sign

def make_api_request(endpoint, params):
    params['app_key'] = APP_KEY
    params['sign_method'] = 'md5'
    params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    params['v'] = '2.0'
    
    # Optional parameters
    if ACCESS_TOKEN:
        params['session'] = ACCESS_TOKEN
    params['format'] = 'json'  # Default to JSON format
    params['simplify'] = 'true'  # Example: using simplified JSON format
    
    params['sign'] = generate_sign(params)
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def main():
    # Example: Query order list
    method = 'taobao.trades.sold.get'  # Replace with a valid method name
    query_params = {
        'method': method
        # Add other specific parameters for your API call here
    }
    
    # Make API request to Taobao API
    response = make_api_request(SECURE_REST_API_ENDPOINT, query_params)
    
    if response:
        print("API Response:")
        print(response)
    else:
        print("Failed to get API response.")

if __name__ == "__main__":
    main()
