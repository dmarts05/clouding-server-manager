import click
from dotenv import load_dotenv

from .list_servers import list_servers


@click.group()
def clouding_server_manager_commands():
    pass


# Add the commands to the group
clouding_server_manager_commands.add_command(list_servers)

if __name__ == "__main__":
    # Load API key from env variable
    load_dotenv()

    # Run the CLI
    try:
        clouding_server_manager_commands()
    except ValueError as e:
        click.echo(e)
        exit(1)
