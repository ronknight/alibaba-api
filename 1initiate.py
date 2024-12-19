import os
import hashlib
import datetime
import urllib.parse
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import time

# Load environment variables from .env file
load_dotenv()

# Function to generate the sign parameter
def generate_sign(params, app_secret):
    # Sort parameters by key
    sorted_params = sorted(params.items())
    
    # Concatenate all key-value pairs
    sign_string = app_secret
    for key, value in sorted_params:
        sign_string += f"{key}{value}"
    
    # Append app_secret again
    sign_string += app_secret

# Get parameters from environment variables
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')  # Your redirect URI

# URL to redirect the user for authorization
auth_url = f"https://oauth.alibaba.com/authorize?response_type=code&client_id={app_key}&redirect_uri={redirect_uri}&State=1212&view=web&sp=ICBU"

print("Please visit the following URL to authorize the application:")
print(auth_url)

# Get the redirected URL from the user (assuming manual input for simplicity)
redirected_url = input("Please enter the redirected URL after authorization: ")

# Parse the URL to extract the query parameters
parsed_url = urlparse(redirected_url)
query_params = parse_qs(parsed_url.query)

# Extract the authorization code and state
auth_code = query_params.get('code', [None])[0]
state = query_params.get('state', [None])[0]

# Print extracted values
print(f"Authorization Code: {auth_code}")
print(f"State: {state}")

# Ensure AUTH_CODE and STATE are available
if not auth_code or not state:
    print("Authorization code or state is missing.")
    exit(1)

# Read the current .env file
env_path = '.env'
env_vars = {}
if os.path.exists(env_path):
    with open(env_path, 'r') as env_file:
        for line in env_file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key] = value

# Update the env_vars with new values
env_vars['AUTH_CODE'] = auth_code
env_vars['STATE'] = state

# Write the updated environment variables back to the .env file
with open(env_path, 'w') as env_file:
    for key, value in env_vars.items():
        env_file.write(f'{key}={value}\n')

print("Authorization code and state have been updated in the .env file.")

# Ensure APP_SECRET is set
if not app_secret:
    print("APP_SECRET is missing or not set.")
    exit(1)

# Generate timestamp
timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d+%H%%3A%M%%3A%S')  # Format timestamp according to URL encoding

# Construct parameters dictionary
params = {
    'app_key': app_key,
    'method': 'taobao.top.auth.token.create',
    'v': '2.0',
    'sign_method': 'md5',
    'format': 'json',
    'timestamp': timestamp,
    'partner_id': 'top-apitools',
    'code': auth_code,
    'uuid': '4sgm'  # Hardcoded value according to the provided URL
}

# Generate sign
sign = generate_sign(params, app_secret)
params['sign'] = sign