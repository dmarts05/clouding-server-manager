from typing import List

import requests

# def send_request(api_key: str, action: Action, target: str) -> requests.Response:
#     """Send the request to the API"""
#     # Build the headers
#     headers = {"Content-Type": "application/json", "X-API-KEY": api_key}

#     # Build the url depending on the action
#     if action == Action.ARCHIVE:
#         url = f"https://api.clouding.io/v1/servers/{target}/archive"
#         response = requests.post(url, headers=headers)
#     elif action == Action.UNARCHIVE:
#         url = f"https://api.clouding.io/v1/servers/{target}/unarchive"
#         response = requests.post(url, headers=headers)
#     elif action == Action.LIST:
#         url = "https://api.clouding.io/v1/servers"
#         response = requests.get(url, headers=headers)
#     else:
#         print("Error: Invalid action specified.")
#         exit(1)

#     return response


def get_all_server_ids(api_key: str) -> List[str]:
    """Get all server ids from the API"""
    # Build the headers
    headers = {"Content-Type": "application/json", "X-API-KEY": api_key}

    # Build list servers url
    url = "https://api.clouding.io/v1/servers"

    # Send the request
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Get the json response
    json_response = response.json()

    # Get the server ids
    server_ids = [server["id"] for server in json_response["servers"]]

    return server_ids
