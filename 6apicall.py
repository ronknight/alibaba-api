import requests
import hashlib
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from urllib.parse import quote_plus
import json
import base64


load_dotenv()

# Alibaba.com API Access Credentials
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
product_id = "11000016025367" 

def update_env_var(key, value, env_file='.env'):
    """Update or create an environment variable in a .env file."""
    dotenv_file = dotenv.find_dotenv(env_file)
    dotenv.load_dotenv(dotenv_file)

    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    os.environ[key] = value 
    dotenv.set_key(dotenv_file, key, value)


# --- Make the API call ---

# API Configuration
base_url = "https://api.taobao.com/router/rest"
method = "taobao.item.seller.get"
api_version = "2.0"

# Prepare API request parameters
timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
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

# Generate the signature
# Sort parameters first
sorted_params = sorted(params.items())
# Construct the string to be signed
sign_str = app_secret + ''.join(
    f"{k}{v}" for k, v in sorted_params
) + app_secret  # Include app_secret at the end
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

# Update the params with the generated signature
params['sign'] = sign

print(params)
# Make the API request
try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    response_data = response.json()
    if "error_response" in response_data:
        # Handle Alibaba API specific errors
        error_code = response_data["error_response"]["code"]
        error_msg = response_data["error_response"]["msg"]
        raise Exception(f"Alibaba API Error: {error_code} - {error_msg}")

    # --- Save the response to a file ---
    with open('response.json', 'w') as f:
        json.dump(response_data, f, indent=4)  # Save the API response as JSON

    # Check if 'result' exists in response_data 
    if "item" in response_data:
        result_item = response_data["item"]
        result_item["images"] = [base64.b64decode(image_str) for image_str in result_item.get("images", [])]


        # --- Extract and Update ACCESS_TOKEN ---
        access_token = response_data["access_token"]  
        update_env_var("ACCESS_TOKEN", access_token)
        print(result_item)


        # Optional: Verification 
        dotenv.load_dotenv('.env')
        print("Updated ACCESS_TOKEN:", os.getenv("ACCESS_TOKEN"))
    else:
        # Handle the case where 'access_token' is not found
        print("Error: 'item' not found in the response")
        print("Response Data:", response_data)
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON response: {e}")
    print(f"Raw response: {response.text}")
    exit(1)
