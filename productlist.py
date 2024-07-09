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

# Command-line arguments
if len(sys.argv) != 4 or sys.argv[2] not in ['10', '20', '30']:
    print("Usage: script.py <subject> <page_size> <page_number>")
    print("Subject is the product title to be looked up.")
    print("Page size options: 10, 20, 30")
    sys.exit(1)

subject = sys.argv[1]
page_size = sys.argv[2]
page_number = sys.argv[3]

# API endpoint and parameters
url = 'https://eco.taobao.com/router/rest'
params = {
    'app_key': app_key,
    'format': 'json',
    'method': 'alibaba.icbu.product.list',
    'partner_id': 'apidoc',
    'session': session_key,
    'sign_method': 'md5',
    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
    'v': '2.0',
    'current_page': page_number,
    'page_size': page_size,
    'subject': subject,
    'language': 'ENGLISH',
}

# Calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Add sign to parameters
params['sign'] = calculate_sign(params, app_secret)

# Remove sensitive information for logging
def remove_sensitive_info(params):
    safe_params = params.copy()
    safe_params.pop('app_key', None)
    safe_params.pop('session', None)
    safe_params.pop('sign', None)
    return safe_params

# Create logs directory if it doesn't exist
log_dir = 'api_logs'
os.makedirs(log_dir, exist_ok=True)

try:
    # Make POST request
    response = requests.post(url, data=params)

    # Log the request details with timestamp (sensitive info removed)
    request_time = time.strftime("%Y-%m-%d %H:%M:%S")
    productlist_request_log = {
        "Request Time": request_time,
        "Request URL": url,
        "Request Method": "POST",
        "Request Headers": remove_sensitive_info(params)
    }

    with open(os.path.join(log_dir, 'productlist_request_log.txt'), 'a') as f:
        f.write(json.dumps(productlist_request_log, indent=4) + "\n\n")

    # Log the response details with timestamp
    response_time = time.strftime("%Y-%m-%d %H:%M:%S")
    productlist_response_log = {
        "Response Time": response_time,
        "Response Status Code": response.status_code,
        "Response Headers": dict(response.headers),
        "Response Body": response.text
    }

    with open(os.path.join(log_dir, 'productlist_response_log.txt'), 'a') as f:
        f.write(json.dumps(productlist_response_log, indent=4) + "\n\n")

    # Check response status code
    if response.status_code == 200:
        try:
            # Parse JSON response
            data = response.json()

            # Check if error response
            if 'error_response' in data:
                error = data['error_response']
                code = error.get('code', '')
                msg = error.get('msg', '')
                sub_msg = error.get('sub_msg', '')
                print(f"API Error: {msg}. {sub_msg}")

                # Log error details
                error_log = {
                    "Error Time": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "Error Code": code,
                    "Error Message": msg,
                    "Error Sub Message": sub_msg
                }
                with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
                    f.write(json.dumps(error_log, indent=4) + "\n\n")
            else:
                # Save response body to JSON file
                response_json_filename = os.path.join(log_dir, f'productlist_response_{response_time.replace(":", "").replace(" ", "_")}.json')
                with open(response_json_filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                # Check if expected response structure is present
                if 'alibaba_icbu_product_list_response' in data:
                    product_list_response = data['alibaba_icbu_product_list_response']
                    products = product_list_response.get('products', {}).get('alibaba_product_brief_response', [])
                    if isinstance(products, list):
                        for product in products:
                            if isinstance(product, dict):
                                subject = product.get('subject', '')
                                print(f"Product Subject: {subject}")
                            else:
                                print("Invalid product structure.")
                    else:
                        print("No products found in response.")
                else:
                    print("Unexpected JSON structure: alibaba_icbu_product_list_response not found.")
        except json.JSONDecodeError as je:
            print(f"Failed to parse JSON response: {je}")
            # Log JSON decoding error
            error_log = {
                "JSON Decode Error Time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "Error Message": str(je)
            }
            with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
                f.write(json.dumps(error_log, indent=4) + "\n\n")
    else:
        print(f"Request failed with status code: {response.status_code}")
        # Log request failure
        failure_log = {
            "Request Failure Time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "Status Code": response.status_code
        }
        with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
            f.write(json.dumps(failure_log, indent=4) + "\n\n")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    # Log request exception
    exception_log = {
        "Request Exception Time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "Exception Message": str(e)
    }
    with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
        f.write(json.dumps(exception_log, indent=4) + "\n\n")
