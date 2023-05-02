import os
import requests

if __name__ == "__main__":
    # Get the server id and api key from environment variables
    server_id = os.environ.get("CLOUDING_SERVER_ID")
    api_key = os.environ.get("CLOUDING_API_KEY")

    # Check if the server id and api key are valid
    if server_id is None or api_key is None:
        print(
            "Please set the CLOUDING_SERVER_ID and CLOUDING_API_KEY environment variables")
        exit(1)

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
