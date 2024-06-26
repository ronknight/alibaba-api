import os
import requests
from dotenv import load_dotenv
import hashlib
import time
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
AUTH_CODE = os.getenv('AUTH_CODE')

ALIBABA_SERVER_CALL_ENTRY = "https://eco.taobao.com/router/rest"
LOG_DIR = 'api_logs/'  # Directory to store log files

# Create directory if it does not exist
os.makedirs(LOG_DIR, exist_ok=True)

# Create a sign
def create_sign(params, secret):
    sorted_params = sorted(params.items())
    basestring = secret + ''.join(f'{k}{v}' for k, v in sorted_params) + secret
    return hashlib.md5(basestring.encode('utf-8')).hexdigest().upper()

# Prepare the request parameters
params = {
    'method': 'taobao.top.auth.token.create',
    'app_key': APP_KEY,
    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
    'format': 'json',
    'v': '2.0',
    'sign_method': 'md5',
    'code': AUTH_CODE
}

# Generate the sign
params['sign'] = create_sign(params, APP_SECRET)

# Make the request
response = requests.get(ALIBABA_SERVER_CALL_ENTRY, params=params)

# Check if the response is successful
if response.status_code == 200:
    response_data = response.json()
    
    # Extract access_token from the response
    try:
        token_result = response_data['top_auth_token_create_response']['token_result']
        token_result_dict = json.loads(token_result)
        access_token = token_result_dict.get('access_token')
        
        if access_token:
            # Update .env file with session_key = access_token
            with open('.env', 'a') as env_file:
                env_file.write(f"\nSESSION_KEY={access_token}")
            
            print(f"Session key (access_token) saved to .env file")
        else:
            print("Access token not found in the response")
    
    except KeyError:
        print("Invalid response format, access token could not be extracted")
    
    # Optionally, save the entire response to a log file or process further
    
else:
    print(f"Failed to retrieve data: {response.status_code}")
