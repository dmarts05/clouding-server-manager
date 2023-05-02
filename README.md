# Clouding Server Manager
A simple Python script for managing Clouding servers.
## Arguments
* `--action`: specify the action to perform.
  * `list`: lists all servers in your Clouding account.
  * `archive`: archives a server.
  * `unarchive`: unarchives a server.
* `--server-id`: "server ID" to perform the action or "all" if you want to perform the action to every server.
## Environment Variables
This script needs a .env file storing your Clouding API key. Simply rename the .env.sample file to .env and replace "YOUR API KEY" with your Clouding API key.
