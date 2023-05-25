"""This module contains the list_servers command function, which lists all servers or some of them"""
import json
from typing import Any, Dict, List, Tuple

import click
import requests

from .constants import BASE_URL


@click.command()
@click.option(
    "--api-key",
    "-k",
    type=str,
    required=True,
    help="The API key to use. If not specified directly, the program will try to load the env variable 'CLOUDING_API_KEY'.",  # noqa: E501
    envvar="CLOUDING_API_KEY",
)
@click.option(
    "--targets",
    "-t",
    type=str,
    required=True,
    multiple=True,
    help="The target server or servers to perform the action on. It can either be a single server id, multiple server ids (-t x -t y -t z ...) or all if you want to perform the action on all servers",  # noqa: E501
)
@click.option(
    "--fields",
    "-f",
    type=str,
    required=False,
    default=None,
    multiple=True,
    help="The fields to show. You can either filter by a single field (-f x) or multiple fields (-f x -f y -f z ...). If not specified, all fields will be shown.",  # noqa: E501
)
def list_servers(api_key: str, targets: Tuple[str], fields: Tuple[str]) -> None:
    """
    List all servers or some of them

    Args:
        api_key: The API key to use
        targets: The target server or servers to perform the action on

    Raises:
        requests.RequestException: If there was an error with any of the requests
    """
    HEADERS = {"Content-Type": "application/json", "X-API-KEY": api_key}
    REQUEST_URL = f"{BASE_URL}/servers"

    responses_json: List[Dict[str, Any]] = []
    # Check if the user wants to list all servers or just some of them
    if "all" in targets:
        response = requests.get(REQUEST_URL, headers=HEADERS)
        if response.status_code == 200:
            for server in response.json()["servers"]:
                responses_json.append(server)
        else:
            raise requests.RequestException(f"Error: {response.status_code} {response.reason}")
    else:
        for target in targets:
            response = requests.get(f"{REQUEST_URL}/{target}", headers=HEADERS)
            if response.status_code == 200:
                responses_json.append(response.json())
            else:
                raise requests.RequestException(f"Error: {response.status_code} {response.reason}")

    # Filter the fields if the user specified any
    if fields:
        responses_json = [{field: server.get(field, "") for field in fields} for server in responses_json]

    # Print the response result for each request (only if there were no errors)
    for r_json in responses_json:  # type: ignore
        click.echo(json.dumps(r_json, indent=4, sort_keys=True))
