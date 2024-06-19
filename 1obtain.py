import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app_key = os.getenv("APP_KEY")
redirect_uri = os.getenv("REDIRECT_URI")  # Your redirect URI

# URL to redirect the user for authorization
auth_url = f"https://oauth.alibaba.com/authorize?response_type=code&client_id={app_key}&redirect_uri={redirect_uri}&State=1212&view=web&sp=ICBU"

print("Please visit the following URL to authorize the application:")
print(auth_url)