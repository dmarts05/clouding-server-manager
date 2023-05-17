import argparse
import time
import os
from pprint import pprint
from typing import List

import requests
from dotenv import load_dotenv


def parse_arguments() -> argparse.Namespace:
    """Parse the arguments passed to the script"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--action",
        required=True,
        choices=["list", "archive", "unarchive"],
        help="Specify the action to perform.",
    )
    parser.add_argument(
        "--server-id",
        help=(
            "[Optional] Specify the server ID to perform the action or 'all'"
            " if you want to apply the action to every server."
        ),
    )

    args = parser.parse_args()
    return args


def send_request(
    api_key: str, action: str, server_id: str
) -> requests.Response:
    """Send the request to the API"""
    # Build the headers
    headers = {"Content-Type": "application/json", "X-API-KEY": api_key}

    # Build the url depending on the action
    if action == "archive":
        url = f"https://api.clouding.io/v1/servers/{server_id}/archive"
        response = requests.post(url, headers=headers)
    elif action == "unarchive":
        url = f"https://api.clouding.io/v1/servers/{server_id}/unarchive"
        response = requests.post(url, headers=headers)
    elif action == "list":
        url = "https://api.clouding.io/v1/servers"
        response = requests.get(url, headers=headers)
    else:
        print("Error: Invalid action specified.")
        exit(1)

    return response


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


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Parse program arguments
    args = parse_arguments()

    # Get api key from environment variables
    api_key = os.environ.get("CLOUDING_API_KEY")

    # Check if the api key is set
    if api_key is None:
        print("Please set the CLOUDING_API_KEY environment variable.")
        exit(1)

    # Send request or requests to the API depending on the action
    if args.server_id == "all" and not args.action == "list":
        server_ids = get_all_server_ids(api_key)
        responses = [
            send_request(api_key, args.action, server_id)
            for server_id in server_ids
            if time.sleep(1) is None  # add a 1 second delay between requests
        ]
    else:
        responses = [send_request(api_key, args.action, args.server_id)]

    # Print the response for each request
    for response in responses:
        pprint(response.json())
