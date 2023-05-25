import click
import requests
from dotenv import load_dotenv

from .commands import archive_servers, list_servers, unarchive_servers


@click.group()
def commands():
    pass


# Add the commands to the group
commands.add_command(archive_servers)
commands.add_command(list_servers)
commands.add_command(unarchive_servers)

if __name__ == "__main__":
    # Load API key from env variable
    load_dotenv()

    # Run the CLI
    try:
        commands()
    except requests.RequestException as e:
        click.secho(e, fg="red")
        exit(1)
