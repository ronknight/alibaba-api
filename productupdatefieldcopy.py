import os
import sys
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

# Define the log directory
LOG_DIR = 'api_logs/'  # Directory to store log files
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if it doesn't exist

# API endpoint and parameters
url = 'https://eco.taobao.com/router/rest'

# Check if product_id is provided as command-line argument
if len(sys.argv) < 2:
    print("Usage: python productupdate.py <product_id>")
    sys.exit(1)

product_id = sys.argv[1]  # Get product_id from command-line argument

# Example of request parameters for updating specific fields of a product
params = {
    'app_key': app_key,
    'format': 'json',
    'method': 'alibaba.icbu.product.update.field',
    'partner_id': 'apidoc',
    'session': session_key,
    'sign_method': 'md5',
    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
    'v': '2.0',
    'format' : 'json',
    'language': 'ENGLISH',  # Set language to English
    'product_id': product_id,  # Product ID from command-line argument
    'attributes': json.dumps({
        'product_attribute': [
            {
                'attribute_id': -1,
                'attribute_name': 'InternalSKU',
                'value_id': -1,
                'value_name': '12129'  # Updated value for InternalSKU
            }
        ],
    }),
    'product_type': 'sourcing',  # Set product type
}

# Function to calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params if k != 'sign']) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Add sign to parameters
params['sign'] = calculate_sign(params, app_secret)

# Log file names
log_file = f"{LOG_DIR}productupdatefield_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
error_log_file = f"{LOG_DIR}productupdatefield_error_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

try:
    # Make the API request
    product_update_field_request = requests.post(url, params=params)
    product_update_field_response = product_update_field_request.json()

    # Log API request
    with open(log_file, 'w') as f:
        json.dump({
            'request_params': params,
            'response': product_update_field_response,
        }, f, indent=4)

    # Example of handling the response data
    if product_update_field_response.get('error_response'):
        with open(error_log_file, 'w') as f:
            json.dump({
                'request_params': params,
                'response': product_update_field_response,
            }, f, indent=4)
        print(f"Error: {product_update_field_response['error_response']['msg']}")
    else:
        print("Product update field API call successful.")
        # Process your response data as needed

except requests.exceptions.RequestException as e:
    with open(error_log_file, 'w') as f:
        json.dump({
            'request_params': params,
            'error_message': str(e),
        }, f, indent=4)
    print(f"Request failed: {e}")
