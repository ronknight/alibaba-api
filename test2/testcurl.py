import requests
from dotenv import load_dotenv
import os
import datetime
import hashlib

# Load environment variables from .env file
load_dotenv()

# Get environment variables
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
auth_code = os.getenv("AUTH_CODE")

# Generate timestamp
timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d+%H%%3A%M%%3A%S')  # Format timestamp according to URL encoding

# Function to generate the sign
def generate_sign(params, secret):
    sorted_params = sorted(params.items())
    concatenated_string = secret + ''.join(f'{k}{v}' for k, v in sorted_params) + secret
    return hashlib.md5(concatenated_string.encode('utf-8')).hexdigest().upper()

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

# Make the GET request
url = "https://gw.api.taobao.com/router/rest"
response = requests.get(url, params=params)

# Print response
print(response.status_code)
print(response.json())
