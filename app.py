from flask import Flask, request, jsonify
import os
import requests
import hashlib
import time
import json
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
session_key = os.getenv('SESSION_KEY')

# Define the log directory
LOG_DIR = 'api_logs/'  # Directory to store log files
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if it doesn't exist

# API endpoint
url = 'https://eco.taobao.com/router/rest'

@app.route('/api/productget', methods=['GET'])
def get_product():
    product_id = request.args.get('product_id')  # Extract product_id from URL parameters
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    # Generate the timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # API parameters
    params = {
        'app_key': app_key,
        'format': 'json',
        'method': 'alibaba.icbu.product.get',
        'partner_id': 'apidoc',
        'session': session_key,
        'sign_method': 'md5',
        'timestamp': timestamp,
        'v': '2.0',
        'language': 'ENGLISH',
        'product_id': product_id,
    }

    # Calculate sign
    params['sign'] = calculate_sign(params, app_secret)

    # Log file names
    log_file = f"{LOG_DIR}productget_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
    error_log_file = f"{LOG_DIR}productget_error_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

    try:
        # Make the API request
        response = requests.get(url, params=params)
        response_json = response.json()

        # Log API request and response
        with open(log_file, 'w') as f:
            json.dump({
                'request_params': remove_sensitive_info(params),
                'response': response_json,
            }, f, indent=4)

        # Handle API response
        if 'error_response' in response_json:
            with open(error_log_file, 'w') as f:
                json.dump({
                    'request_params': remove_sensitive_info(params),
                    'response': response_json,
                }, f, indent=4)
            return jsonify({"error": response_json['error_response']['msg']}), response.status_code
        else:
            return jsonify(response_json)

    except requests.exceptions.RequestException as e:
        with open(error_log_file, 'w') as f:
            json.dump({
                'request_params': remove_sensitive_info(params),
                'error_message': str(e),
            }, f, indent=4)
        return jsonify({"error": str(e)}), 500

def calculate_sign(params, secret):
    # Sort parameters and generate sign string
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

def remove_sensitive_info(params):
    # Remove sensitive information for logging
    safe_params = params.copy()
    safe_params.pop('app_key', None)
    safe_params.pop('session', None)
    safe_params.pop('sign', None)
    return safe_params

if __name__ == '__main__':
    app.run(debug=True)
