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
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
session_key = os.getenv("SESSION_KEY")

# Define the log directory
LOG_DIR = "api_logs/"  # Directory to store log files
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if it doesn't exist

# API endpoint and parameters
url = "https://eco.taobao.com/router/rest"

# Example of request parameters for adding a product
params = {
    "app_key": app_key,
    "format": "json",
    "method": "alibaba.icbu.product.add",  # Method for adding a product
    "partner_id": "apidoc",
    "session": session_key,
    "sign_method": "md5",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "v": "2.0",
    "category_id": 201951802,
    "subject": "New Product Name",  # Replace with actual product name
    "product_type": "sourcing",  # Set product type
    "language": "ENGLISH",  # Set language to English
    "keywords": json.dumps({
        "string": [
            "Product Keywords"
        ]
    }),
    "main_image": json.dumps({
        "images": [
            "https://example.com/product_image.jpg"
        ]
    }),
    "attributes": json.dumps({
        "product_attribute": [
            {
                "attribute_id": -1,
                "attribute_name": "InternalSKU",
                "value_id": -1,
                "value_name": "12129"
            }
        ]
    })
}

# Function to calculate sign
def calculate_sign(params, secret):
    # Sort parameters by keys
    sorted_params = sorted(params.items())
    
    # Construct sign string
    sign_string = secret + ''.join([f"{k}{v}" for k, v in sorted_params if k != "sign"]) + secret
    
    # Calculate MD5 hash and convert to uppercase
    calculated_sign = hashlib.md5(sign_string.encode("utf-8")).hexdigest().upper()
    return calculated_sign

# Add sign to parameters
params["sign"] = calculate_sign(params, app_secret)

# Log file names
log_file = f"{LOG_DIR}productadd_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
error_log_file = f"{LOG_DIR}productadd_error_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

try:
    # Make the API request
    product_add_request = requests.post(url, params=params)
    product_add_response = product_add_request.json()

    # Log API request
    with open(log_file, "w") as f:
        json.dump({
            "request_params": params,
            "response": product_add_response,
        }, f, indent=4)

    # Example of handling the response data
    if product_add_response.get("error_response"):
        with open(error_log_file, "w") as f:
            json.dump({
                "request_params": params,
                "response": product_add_response,
            }, f, indent=4)
        print(f"Error: {product_add_response['error_response']['msg']}")
    else:
        print("Product add API call successful.")
        # Process your response data as needed

except requests.exceptions.RequestException as e:
    with open(error_log_file, "w") as f:
        json.dump({
            "request_params": params,
            "error_message": str(e),
        }, f, indent=4)
    print(f"Request failed: {e}")
