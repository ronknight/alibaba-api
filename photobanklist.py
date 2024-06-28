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

# Command-line arguments
if len(sys.argv) != 2:
    print("Usage: script.py <page_size>")
    print("page_size is the number of items per page to fetch (e.g., 500)")
    sys.exit(1)

page_size = sys.argv[1]

# API endpoint and parameters
url = 'https://eco.taobao.com/router/rest'
params = {
    'app_key': app_key,
    'format': 'json',
    'method': 'alibaba.icbu.photobank.list',
    'partner_id': 'apidoc',
    'session': session_key,
    'sign_method': 'md5',
    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
    'v': '2.0',
    'current_page': '1',
    'page_size': page_size,
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
    request_time = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(LOG_DIR, 'photobanklist_request_log.txt'), 'a') as f:
        f.write(f"Request Time: {request_time}\n")
        f.write(f"Request URL: {url}\n")
        f.write(f"Request Method: POST\n")
        f.write("Request Headers:\n")
        for key, value in params.items():
            f.write(f"{key}: {value}\n")
        f.write("Request Body:\n")
        f.write(json.dumps(params) + "\n\n")

    # Make POST request
    response = requests.post(url, data=params)

    # Log the response details
    response_time = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(LOG_DIR, 'photobanklist_response_log.txt'), 'a') as f:
        f.write(f"Response Time: {response_time}\n")
        f.write(f"Response Status Code: {response.status_code}\n")
        f.write("Response Headers:\n")
        for key, value in response.headers.items():
            f.write(f"{key}: {value}\n")
        f.write("Response Body:\n")
        f.write(response.text + "\n\n")

    # Check response status code and save response to JSON file if successful
    if response.status_code == 200:
        try:
            data = response.json()
            response_json_filename = f'photobanklist_response_{response_time.replace(":", "").replace(" ", "_")}.json'
            response_json_path = os.path.join(LOG_DIR, response_json_filename)
            with open(response_json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        except json.JSONDecodeError as je:
            error_msg = f"Failed to parse JSON response: {je}"
            print(error_msg)
            with open(os.path.join(LOG_DIR, 'photobanklist_error_log.txt'), 'a') as f:
                f.write(f"{error_msg}\n")

    else:
        # Log request failure
        failure_log = f"Request Failure Time: {response_time}\n"
        failure_log += f"Status Code: {response.status_code}\n"
        with open(os.path.join(LOG_DIR, 'photobanklist_error_log.txt'), 'a') as f:
            f.write(failure_log)
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    request_error_msg = f"Request error: {e}"
    print(request_error_msg)
    with open(os.path.join(LOG_DIR, 'photobanklist_error_log.txt'), 'a') as f:
        f.write(f"{request_error_msg}\n")

except Exception as e:
    general_error_msg = f"Error occurred: {e}"
    print(general_error_msg)
    with open(os.path.join(LOG_DIR, 'photobanklist_error_log.txt'), 'a') as f:
        f.write(f"{general_error_msg}\n")
