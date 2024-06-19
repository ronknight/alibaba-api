import requests
from dotenv import load_dotenv
import os
import time
import hashlib

# Load environment variables from .env file
load_dotenv()

# Define API endpoint and method
url = "https://eco.taobao.com/router/rest"  # Ensure this is the correct endpoint

# Load API credentials from environment variables
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
access_token = os.getenv("ACCESS_TOKEN")

# Print access token for debugging (remove this in production)
print(f"Access Token: {access_token}")

# Check if access token is empty or None
if not access_token:
    raise ValueError("Access token is missing. Please check your .env file.")

# Generate current timestamp in required format
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

# Define other necessary parameters
method = "alibaba.icbu.product.get"  # Ensure this is the correct method name
v = "2.0"
sign_method = "md5"
format = "json"

# Prepare the payload with necessary parameters
payload = {
    "method": method,
    "app_key": app_key,
    "timestamp": timestamp,
    "v": v,
    "sign_method": sign_method,
    "format": format,
    "access_token": access_token
}

# Step 1: Concatenate parameters for signing
sorted_params = sorted(payload.items())
concatenated_params = "".join(f"{k}{v}" for k, v in sorted_params)
string_to_sign = f"{app_secret}{concatenated_params}{app_secret}"

# Step 2: Hash the concatenated string using MD5
md5_hash = hashlib.md5(string_to_sign.encode())

# Step 3: Convert the hash to uppercase to get the signature
signature = md5_hash.hexdigest().upper()

# Add the signature to the payload
payload["sign"] = signature

# Set headers if needed (empty in this case)
headers = {}

# Make the POST request to the API
response = requests.post(url, headers=headers, data=payload)

# Print the response text for debugging
print(response.text)
