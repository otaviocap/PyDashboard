from cgitb import text
import json
import time
import random
from rich.panel import Panel
from rich.live import Live
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, TextColumn
from rich.progress_bar import ProgressBar
from rich import box
from utils import mod

from Connector import Connector

class Dashboard:
	
	topics: list
	data: dict
	connector: Connector

	def __init__(self, console: Console, connector: Connector, topics: list):
		self.topics = topics
		self.console = console
		self.connector = connector
		self.data = {}
	
		def update(topic, value):
			self.data[topic] = value

		self.connector.on_message = update

		for i in self.topics:
			self.data[i["topic"]] = 0


	def render(self, topic):
		if topic["render"] == "value":
			return str(self.data[topic["topic"]])
		
		if topic["render"]== "progress":
			options = [int(i) for i in topic["options"].split(",")]

			bar = ProgressBar(total=mod(options[0]) + mod(options[1]))

			bar.update(completed=(self.data[topic["topic"]]+mod(options[0])))

			return bar

	def connecting_page(self):
		with Progress(
			SpinnerColumn("moon"),
			TimeElapsedColumn(),
			TextColumn("[progress.description]{task.description}"),
			console=self.console,
			transient=True
		) as progress:
			taskId = progress.add_task("[cyan]Connecting to MQTT Broker...", total=1, start=True)
			self.connector.on_connection = lambda: progress.advance(taskId)
			self.connector.connect()

			while not progress.finished:
				time.sleep(1)
			


	def main_page(self):
		with Live(console=self.console, refresh_per_second=5) as live:
			while True:
				table = Table(expand=True, box=box.SIMPLE_HEAD)

				table.add_column("Topic", width=15, justify="left")
				table.add_column("Value", width=25, justify="center")

				for i in self.topics:
					
					table.add_row(
						"[green]"+i["topic"].capitalize()+f"[cyan] ({ self.data[i['topic']] }) ", 
						self.render(i)
					)

				live.update(Panel(
					table,
					title="MQTT Dashboard",
					subtitle="(ctrl+c to exit)",
					subtitle_align="left",
				))

				time.sleep(1)

	def run(self):
		self.connecting_page()
		self.main_page()
		
	def toJson(self):
		return json.dumps(self, default = lambda e: e.__dict__, indent=4)

	def __str__(self):
		return self.toJson()


if __name__ == "__main__":
	from Connector import Connector

	console = Console()
	data = []

	with open("credentials.json", "r") as file:
		data = json.loads(file.read())
	
	connection = Connector(console, **data)
	dashboard = Dashboard(console, connection, data["topics"])
	dashboard.run()