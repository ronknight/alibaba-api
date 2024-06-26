import os
import requests
import hashlib
import time
import urllib.parse
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
params = {
    'app_key': app_key,
    'format': 'json',  # Request JSON format
    'method': 'alibaba.icbu.product.list',  # API method
    'partner_id': 'apidoc',
    'session': session_key,
    'sign_method': 'md5',  # Sign method MD5
    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
    'v': '2.0',
    'current_page': '1',  # Example: Set current page
    'page_size': '10',    # Example: Set page size
    'subject': '',     # Example: Product name query
    'language': 'ENGLISH',
}

# Calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Add sign to parameters
params['sign'] = calculate_sign(params, app_secret)

try:
    # Log the request details
    print(f"Request URL: {url}")
    print(f"Request Method: POST")
    print("Request Headers:")
    for key, value in params.items():
        print(f"{key}: {value}")
    print("Request Body:")
    print(params)

    # Make POST request
    response = requests.post(url, data=params)

    # Log the response details
    print(f"Response Status Code: {response.status_code}")
    print("Response Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("Response Body:")
    print(response.text)

    # Check if request was successful
    if response.status_code == 200:
        try:
            # Parse JSON response
            data = response.json()

            # Check if error response
            if 'error_response' in data:
                error = data['error_response']
                code = error['code']
                msg = error['msg']
                sub_msg = error['sub_msg'] if 'sub_msg' in error else ''
                print(f"API Error: {msg}. {sub_msg}")
            else:
                # Check if expected response structure is present
                if 'alibaba_icbu_product_list_response' in data:
                    product_list_response = data['alibaba_icbu_product_list_response']
                    products = product_list_response.get('products', [])
                    if products:
                        for product in products:
                            subject = product.get('subject', '')
                            print(f"Product Subject: {subject}")
                    else:
                        print("No products found in response.")
                else:
                    print("Unexpected JSON structure: alibaba_icbu_product_list_response not found.")
        except json.JSONDecodeError as je:
            print(f"Failed to parse JSON response: {je}")
    else:
        print(f"Request failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
