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

# Check if group_name and operation are provided as command-line arguments
if len(sys.argv) < 3:
    print("Usage: python script.py <group_name> <operation>")
    print("Group_name can be any name. Operation options are 'add', 'delete' or 'rename'.")
    sys.exit(1)

group_name = sys.argv[1]  # Get group_name from command-line argument
operation = sys.argv[2]  # Get operation from command-line argument

# Optional parameters
photo_group_operation_request = {
    "group_name": group_name,
    "operation": operation
}

# Convert the request object to a JSON string
photo_group_operation_request_json = json.dumps(photo_group_operation_request)

params = {
    "app_key": app_key,
    "format": "json",
    "method": "alibaba.icbu.photobank.group.operate",
    "partner_id": "apidoc",
    "session": session_key,
    "sign_method": "md5",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "v": "2.0",
    "photo_group_operation_request": photo_group_operation_request_json,
}

# Calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Add sign to parameters
params["sign"] = calculate_sign(params, app_secret)

# Remove sensitive information for logging
def remove_sensitive_info(params):
    safe_params = params.copy()
    safe_params.pop('app_key', None)
    safe_params.pop('session', None)
    safe_params.pop('sign', None)
    return safe_params

# Log file names
log_file = f"{LOG_DIR}photobankgroupoperate_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
error_log_file = f"{LOG_DIR}photobankgroupoperate_error_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

try:
    # Make the API request
    getphotobankgroupoperate_request = requests.get(url, params=params)
    getphotobankgroupoperate_response = getphotobankgroupoperate_request.json()

    # Log API request
    with open(log_file, 'w') as f:
        json.dump({
            "request_params": remove_sensitive_info(params),
            "response": getphotobankgroupoperate_response,
        }, f, indent=4)

    # Example of handling the response data
    if getphotobankgroupoperate_response.get("error_response"):
        with open(error_log_file, 'w') as f:
            json.dump({
                "request_params": remove_sensitive_info(params),
                "response": getphotobankgroupoperate_response,
            }, f, indent=4)
        print(f"Error: {getphotobankgroupoperate_response['error_response']['msg']}")
    else:
        print("API call successful.")
        # Process your response data as needed

except requests.exceptions.RequestException as e:
    with open(error_log_file, 'w') as f:
        json.dump({
            "request_params": remove_sensitive_info(params),
            "error_message": str(e),
        }, f, indent=4)
    print(f"Request failed: {e}")
