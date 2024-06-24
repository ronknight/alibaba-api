import requests
import hashlib
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
access_token = os.getenv('ACCESS_TOKEN')

# Define API endpoint and method
base_url = "https://api.taobao.com/router/rest"
method = "taobao.item.seller.get"
api_version = "2.0"

# Get current UTC time
timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Define other parameters
product_id = "11000016025367"  # Replace with your actual product ID
params = {
    'method': method,
    'app_key': app_key,
    'session': access_token,
    'timestamp': timestamp,
    'format': 'json',
    'v': api_version,
    'sign_method': 'md5',
    'fields': 'num_iid,title,nick,price,num',
    'num_iid': product_id
}

# Generate the sign
sorted_params = sorted(params.items())
sign_str = app_secret + ''.join([f'{k}{v}' for k, v in sorted_params])
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

# Add sign to params
params['sign'] = sign

# Make the API request
try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise error for bad status codes
    data = response.json()
    print(data)  # Output the retrieved data
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
