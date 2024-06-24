from urllib.parse import urlparse, parse_qs

# Given URL
url = "https://cbk.4sgm.us/?code=1_J3LNDUnqkQeDmjr6JY35XRQ41070&state=1212"

# Parse the URL to extract the query parameters
parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

# Extract the authorization code
auth_code = query_params.get('code', [None])[0]
state = query_params.get('state', [None])[0]

print(f"Authorization Code: {auth_code}")
print(f"State: {state}")
