import requests
from dotenv import load_dotenv
import os
import requests
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()


url = "https://api.taobao.com/router/rest?method=alibaba.icbu.product.get"
app_key = os.getenv("APP_KEY")
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


headers = {}
response = requests.post(url, headers=headers, data=payload)
print(response.text)
