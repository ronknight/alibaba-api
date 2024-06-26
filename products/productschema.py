import os
import requests
import hashlib
import time
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
session_key = os.getenv('SESSION_KEY')

# API endpoint and parameters
url = 'http://gw.api.taobao.com/router/rest'
method = 'alibaba.icbu.product.schema.get'
format = 'json'  # Response format
sign_method = 'md5'
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
v = '2.0'

# Additional parameters specific to the API method
params = {
    'app_key': app_key,
    'method': method,
    'format': format,
    'sign_method': sign_method,
    'timestamp': timestamp,
    'v': v,
    'session': session_key  # Include session key here
}

# Calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Add sign to parameters
params['sign'] = calculate_sign(params, app_secret)

try:
    # Make POST request
    response = requests.post(url, data=params)

    # Check if request was successful
    if response.status_code == 200:
        try:
            # Parse JSON response
            data = response.json()

            # Check for error response
            if 'error_response' in data:
                error = data['error_response']
                code = error['code']
                msg = error['msg']
                sub_msg = error.get('sub_msg', '')
                print(f"API Error: {msg}. {sub_msg}")
            else:
                # Process successful response
                print("Successful Response:")
                print(json.dumps(data, indent=2))

        except json.JSONDecodeError as je:
            print(f"Failed to parse JSON response: {je}")

    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
