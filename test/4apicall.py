import time
import hashlib

url = "https://eco.taobao.com/router/rest"  # Ensure this is the correct endpoint

# Use the newly obtained access token
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

method = "alibaba.icbu.product.get"
v = "2.0"
sign_method = "md5"
format = "json"

payload = {
    "method": method,
    "app_key": app_key,
    "timestamp": timestamp,
    "v": v,
    "sign_method": sign_method,
    "format": format,
    "access_token": access_token
}

sorted_params = sorted(payload.items())
concatenated_params = "".join(f"{k}{v}" for k, v in sorted_params)
string_to_sign = f"{app_secret}{concatenated_params}{app_secret}"

md5_hash = hashlib.md5(string_to_sign.encode())
signature = md5_hash.hexdigest().upper()

payload["sign"] = signature

headers = {}
response = requests.post(url, headers=headers, data=payload)
print(response.text)
