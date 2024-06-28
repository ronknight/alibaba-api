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
if len(sys.argv) != 3:
    print("Usage: script.py <subject> <page_size>")
    print("Subject is the product title to be looked up.")
    print('To set subject to blank run command (python productlist.py "" 200)')
    sys.exit(1)

subject = sys.argv[1]
page_size = sys.argv[2]

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
    'current_page': '1',
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

# Create logs directory if it doesn't exist
log_dir = 'api_logs'
os.makedirs(log_dir, exist_ok=True)

try:
    # Log the request details with timestamp
    request_time = time.strftime("%Y-%m-%d %H:%M:%S")
    productlist_request_log = f"Request Time: {request_time}\n"
    productlist_request_log += f"Request URL: {url}\n"
    productlist_request_log += f"Request Method: POST\n"
    productlist_request_log += "Request Headers:\n"
    for key, value in params.items():
        productlist_request_log += f"{key}: {value}\n"
    productlist_request_log += "Request Body:\n"
    productlist_request_log += json.dumps(params) + "\n\n"

    # Make POST request
    response = requests.post(url, data=params)

    # Log the request details
    with open(os.path.join(log_dir, 'productlist_request_log.txt'), 'a') as f:
        f.write(productlist_request_log)

    # Log the response details with timestamp
    response_time = time.strftime("%Y-%m-%d %H:%M:%S")
    productlist_response_log = f"Response Time: {response_time}\n"
    productlist_response_log += f"Response Status Code: {response.status_code}\n"
    productlist_response_log += "Response Headers:\n"
    for key, value in response.headers.items():
        productlist_response_log += f"{key}: {value}\n"
    productlist_response_log += "Response Body:\n"
    productlist_response_log += response.text + "\n\n"

    # Log the response details
    with open(os.path.join(log_dir, 'productlist_response_log.txt'), 'a') as f:
        f.write(productlist_response_log)

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
                error_log = f"Error Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                error_log += f"Error Code: {code}\n"
                error_log += f"Error Message: {msg}\n"
                error_log += f"Error Sub Message: {sub_msg}\n"
                with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
                    f.write(error_log)
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
            error_log = f"JSON Decode Error Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            error_log += f"Error Message: {str(je)}\n"
            with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
                f.write(error_log)
    else:
        print(f"Request failed with status code: {response.status_code}")
        # Log request failure
        failure_log = f"Request Failure Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        failure_log += f"Status Code: {response.status_code}\n"
        with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
            f.write(failure_log)

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    # Log request exception
    exception_log = f"Request Exception Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    exception_log += f"Exception Message: {str(e)}\n"
    with open(os.path.join(log_dir, 'productlist_error_log.txt'), 'a') as f:
        f.write(exception_log)
