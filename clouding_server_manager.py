import os
import requests

# Get the server id and api key from environment variables
server_id = os.environ['CLOUDING_SERVER_ID']
api_key = os.environ['CLOUDING_API_KEY']

# Build the request
url = f"https://api.clouding.io/v1/servers/{server_id}/archive"
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": api_key
}

# Send the request
response = requests.post(url, headers=headers)

# Check the response
if response.ok:
    print("Server archived successfully!")
else:
    print(f"Error archiving server: {response.text}")
