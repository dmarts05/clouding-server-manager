from typing import List

import requests

from .constants import BASE_URL

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
    """
    Get all the server ids

    Args:
        api_key: The API key to use

    Raises:
        requests.RequestException: If there was an error with any of the requests

    Returns:
        A list with all the server ids
    """
    HEADERS = {"Content-Type": "application/json", "X-API-KEY": api_key}
    REQUEST_URL = f"{BASE_URL}/servers"

    response = requests.get(REQUEST_URL, headers=HEADERS)
    if not response.ok:
        raise requests.RequestException(f"Error: {response.status_code} {response.reason}")

    # Return a list with all the server ids
    server_ids = [server["id"] for server in response.json()["servers"]]
    return server_ids
