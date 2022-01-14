import paho.mqtt.client as mqtt
from rich.console import Console

class Connector:

	address: str
	port: int
	username: str
	password: str
	clientId: str

	topics = []

	on_connection = lambda: None
	on_message = lambda: None

	def __init__(
		self, 
		console: Console, 
		address:str, 
		port:str, 
		username:str, 
		password:str, 
		clientId:str, 
		topics: "list[dict[str, str, str]]"
	) -> None:

		self.address = address
		self.port = int(port)
		self.username = username
		self.password = password

		self.console = console
		self.topics = topics

		def on_connection(client, userdata, flags, rc):
			console.log("Connected :star-struck:")

			for i in topics:
				client.subscribe(i["topic"])

			self.on_connection()
		
		def on_message(client, userdata, msg):
			self.on_message(msg.topic, float(msg.payload))

		self.client = mqtt.Client(client_id=clientId)
		self.client.on_connect = on_connection
		self.client.on_message = on_message


	def connect(self):
		self.client.username_pw_set(username=self.username, password=self.password)
		self.client.connect(host=self.address, port=self.port, keepalive=20)
		self.client.loop_start()

	def close_connection(self):
		self.client.loop_stop()

	
