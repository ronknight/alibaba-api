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

# Check if new_display and product_id_list are provided as command-line arguments
if len(sys.argv) < 3:
    print("Usage: python script.py <new_display> <product_id_list>")
    print("New_display options are 'on' and 'off', Product_id_list are encoded product ids.")
    sys.exit(1)

new_display = sys.argv[1]  # Get new_display from command-line argument
product_id_list = sys.argv[2]  # Get product_id_list from command-line argument

# Ensure new_display is either "on" or "off"
if new_display not in ["on", "off"]:
    print("Error: new_display must be 'on' or 'off'")
    sys.exit(1)

# Parameters for the request
params = {
    "app_key": app_key,
    "format": "json",
    "method": "alibaba.icbu.product.batch.update.display",
    "partner_id": "apidoc",
    "session": session_key,
    "sign_method": "md5",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "v": "2.0",
    "new_display": new_display,
    "product_id_list": product_id_list,
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
log_file = f"{LOG_DIR}productbatchupdatedisplay_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
error_log_file = f"{LOG_DIR}productbatchupdatedisplay_error_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

try:
    # Make the API request
    getproductbatchupdatedisplay_request = requests.get(url, params=params)
    getproductbatchupdatedisplay_response = getproductbatchupdatedisplay_request.json()

    # Log API request
    with open(log_file, 'w') as f:
        json.dump({
            "request_params": remove_sensitive_info(params),
            "response": getproductbatchupdatedisplay_response,
        }, f, indent=4)

    # Example of handling the response data
    if getproductbatchupdatedisplay_response.get("error_response"):
        with open(error_log_file, 'w') as f:
            json.dump({
                "request_params": remove_sensitive_info(params),
                "response": getproductbatchupdatedisplay_response,
            }, f, indent=4)
        print(f"Error: {getproductbatchupdatedisplay_response['error_response']['msg']}")
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
