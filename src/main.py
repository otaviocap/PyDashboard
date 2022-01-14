from http import client
import json

from rich.console import Console

from Connector import Connector
from Dashboard import Dashboard
import signal
import sys

if __name__ == "__main__":

	console = Console()
	data = []

	with open("credentials.json", "r") as file:
		data = json.loads(file.read())

	connection = Connector(console, **data)
	dashboard = Dashboard(console, connection, data["topics"])
	
	def signal_handler(sig, frame):
		dashboard.stop = True
		connection.close_connection()
		sys.exit(0)

	signal.signal(signal.SIGINT, signal_handler)
	dashboard.run()
	signal.pause()
	