from http import client
import json

from rich.console import Console

from Connector import Connector
from Dashboard import Dashboard


if __name__ == "__main__":

	console = Console()
	data = []

	with open("credentials.json", "r") as file:
		data = json.loads(file.read())
	
	connection = Connector(console, **data)

	dashboard = Dashboard(console, connection, data["topics"])
	
	dashboard.run()
	
	connection.close_connection()