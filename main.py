import requests
from dotenv import load_dotenv
import os
import time
import hashlib

# Load environment variables from .env file
load_dotenv()

url = "https://api.taobao.com/router/rest?method=alibaba.icbu.product.get"
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
timestamp = str(int(time.time()))  # Generate current timestamp
v = "2.0"
sign_method = "md5"
format = "json"

payload = {
    "app_key": app_key,
    "timestamp": timestamp,
    "v": v,
    "sign_method": sign_method,
    "format": format,
    "access_token": access_token
}

# Step 1: Concatenate parameters
sorted_params = sorted(payload.items())
concatenated_params = "".join(f"{k}{v}" for k, v in sorted_params)
string_to_sign = f"{app_secret}{concatenated_params}{app_secret}"

# Step 2: Hash the string
md5_hash = hashlib.md5(string_to_sign.encode())

# Step 3: Convert to uppercase
signature = md5_hash.hexdigest().upper()

# Add the signature to the payload
payload["sign"] = signature

headers = {}
response = requests.post(url, headers=headers, data=payload)
print(response.text)