import os
import hashlib
import datetime
import urllib.parse
import requests  # Import requests library
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to generate the sign parameter
def generate_sign(params, app_secret):
    # Sort parameters by key
    sorted_params = sorted(params.items())
    
    # Concatenate all key-value pairs
    sign_string = app_secret
    for key, value in sorted_params:
        sign_string += f"{key}{value}"
    
    # Append app_secret again
    sign_string += app_secret
    
    # Calculate MD5 hash
    sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()
    return sign

# Get parameters from environment variables
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
auth_code = os.getenv('AUTH_CODE')
uuid_param = '4sgm'  # Hardcoded value according to the provided URL

if not (app_key and app_secret and auth_code):
    print("Environment variables (APP_KEY, APP_SECRET, AUTH_CODE) are missing or not set.")
else:
    # Generate timestamp
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d+%H%%3A%M%%3A%S')  # Format timestamp according to URL encoding
    
    # Construct parameters dictionary
    params = {
        'app_key': app_key,
        'method': 'taobao.top.auth.token.create',
        'v': '2.0',
        'sign_method': 'md5',
        'format': 'json',
        'timestamp': timestamp,
        'partner_id': 'top-apitools',
        'code': auth_code,
        'uuid': uuid_param
    }
    
    # Generate sign
    sign = generate_sign(params, app_secret)
    params['sign'] = sign
    
    # Construct the exact URL with encoded parameters
    encoded_params = urllib.parse.urlencode(params)
    exact_url_format = f"https://gw.api.taobao.com/router/rest?{encoded_params}"
    
    # Make API call
    try:
        response = requests.get(exact_url_format)
        response.raise_for_status()  # Raise exception for bad response status
        data = response.json()  # Parse JSON response
        print("API Response:", data)
    except requests.exceptions.RequestException as e:
        print("API call failed:", e)
