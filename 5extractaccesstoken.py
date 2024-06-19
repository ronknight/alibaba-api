import dotenv
import os
import json

def update_env_var(key, value, env_file='.env'):
    """Update or create an environment variable in a .env file."""
    dotenv_file = dotenv.find_dotenv(env_file)
    dotenv.load_dotenv(dotenv_file)

    # Remove quotes if they exist before updating
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        value = value[1:-1]  

    os.environ[key] = value 

    # Read the entire file
    with open(dotenv_file, 'r') as f:
        lines = f.readlines()

    # Find and update the line with the key
    with open(dotenv_file, 'w') as f:
        for line in lines:
            if line.startswith(key + '='):
                f.write(f"{key}={value}\n")
            else:
                f.write(line)

# --- Read from response.json ---
with open('response.json', 'r') as f:
    response_data = json.load(f)

# Parse the token_result string as JSON
token_result = json.loads(response_data["top_auth_token_create_response"]["token_result"])

# Extract the access_token
access_token = token_result["access_token"]


# --- Main Update Logic (ACCESS_TOKEN only) ---
update_env_var("ACCESS_TOKEN", access_token)


# Optional: Verification
dotenv.load_dotenv('.env')
print("Updated ACCESS_TOKEN:", os.getenv("ACCESS_TOKEN")) 
