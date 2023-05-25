import json
import time
from typing import Any, Dict, List

import click
import requests

from .constants import BASE_URL, MAX_TOTAL_WAIT_TIME, WAIT_TIME
from .helpers import get_all_server_ids


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
def list_servers(api_key: str, targets: List[str], fields: List[str]) -> None:
    """
    List all clouding servers or some of them by id

    Args:
        api_key: The API key to use
        targets: The target server or servers to perform the action on

    Raises:
        requests.RequestException: If there was an error with any of the requests
    """
    click.secho("[LIST SERVERS] Listing servers...", fg="blue")

    HEADERS = {"Content-Type": "application/json", "X-API-KEY": api_key}
    REQUEST_URL = f"{BASE_URL}/servers"

    responses_json: List[Dict[str, Any]] = []
    # Check if the user wants to list all servers or just some of them by id
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
            if response.ok:
                responses_json.append(response.json())
            else:
                raise requests.RequestException(f"Error: {response.status_code} {response.reason}")

    # Filter the fields if the user specified any
    if fields:
        click.secho("Filtering fields...", fg="blue")
        responses_json = [{field: server.get(field, "Invalid field") for field in fields} for server in responses_json]

    # Print the response result for each request (only if there were no errors)
    for r_json in responses_json:  # type: ignore
        click.echo(json.dumps(r_json, indent=4, sort_keys=True))


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
def archive_servers(api_key: str, targets: List[str]) -> None:
    """
    Archive all clouding servers or some of them by id

    Args:
        api_key: The API key to use
        targets: The target server or servers to perform the action on

    Raises:
        requests.RequestException: If there was an error with any of the requests
    """
    click.secho("[ARCHIVE SERVERS] Archiving servers...", fg="blue")

    HEADERS = {"Content-Type": "application/json", "X-API-KEY": api_key}

    responses_json: List[Dict[str, Any]] = []
    if "all" in targets:
        # Get all server ids if the user wants to unarchive all servers
        targets = get_all_server_ids(api_key)

    # Make unarchive requests until all servers have been unarchived or total wait time is exceeded
    waited_time = 0
    while targets and waited_time < MAX_TOTAL_WAIT_TIME:
        for target in targets:
            response = requests.post(f"{BASE_URL}/servers/{target}/archive", headers=HEADERS)

            if response.ok and response.json()["status"] == "completed":
                responses_json.append(response.json())
                targets.remove(target)
            elif not response.ok:
                click.echo(json.dumps(response.json(), indent=4, sort_keys=True))
                raise requests.RequestException(f"Error: {response.status_code} {response.reason}")

        # Wait some time before making the next batch of requests
        click.secho("[ARCHIVE SERVERS] Some servers are still being archived...", fg="blue")
        click.secho(f"[ARCHIVE SERVERS] Waiting {WAIT_TIME} seconds before checking again...", fg="blue")
        time.sleep(WAIT_TIME)
        waited_time += WAIT_TIME

    click.secho("[ARCHIVE SERVERS] All servers have been archived!", fg="blue")

    # Print the response result for each request (only if there were no errors)
    for r_json in responses_json:  # type: ignore
        click.echo(json.dumps(r_json, indent=4, sort_keys=True))


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
def unarchive_servers(api_key: str, targets: List[str]) -> None:
    """
    Unarchive all clouding servers or some of them by id

    Args:
        api_key: The API key to use
        targets: The target server or servers to perform the action on

    Raises:
        requests.RequestException: If there was an error with any of the requests
    """
    click.secho("[UNARCHIVE SERVERS] Unarchiving servers...", fg="blue")

    HEADERS = {"Content-Type": "application/json", "X-API-KEY": api_key}

    responses_json: List[Dict[str, Any]] = []
    if "all" in targets:
        # Get all server ids if the user wants to unarchive all servers
        targets = get_all_server_ids(api_key)

    # Make unarchive requests until all servers have been unarchived or total wait time is exceeded
    waited_time = 0
    while targets and waited_time < MAX_TOTAL_WAIT_TIME:
        for target in targets:
            response = requests.post(f"{BASE_URL}/servers/{target}/unarchive", headers=HEADERS)

            if response.ok and response.json()["status"] == "completed":
                responses_json.append(response.json())
                targets.remove(target)
            elif not response.ok:
                click.echo(json.dumps(response.json(), indent=4, sort_keys=True))
                raise requests.RequestException(f"Error: {response.status_code} {response.reason}")

        # Wait some time before making the next batch of requests
        click.secho("[UNARCHIVE SERVERS] Some servers are still being unarchived...", fg="blue")
        click.secho(f"[UNARCHIVE SERVERS] Waiting {WAIT_TIME} seconds before checking again...", fg="blue")
        time.sleep(WAIT_TIME)
        waited_time += WAIT_TIME

    click.secho("[UNARCHIVE SERVERS] All servers have been unarchived!", fg="blue")

    # Print the response result for each request (only if there were no errors)
    for r_json in responses_json:  # type: ignore
        click.echo(json.dumps(r_json, indent=4, sort_keys=True))
