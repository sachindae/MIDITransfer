import mido 
import socket
import threading

from constant import SERVER_IP, SERVER_PORT
from parsing import parse_data

# Class for creating a client socket
class Client:

	# Initialize stuff
	def __init__(self, output_port, input_obj):
		#print('init client')

		# Start client thread
		self.start_client_thread()
		self.running = False
		self.input = input_obj
		self.output_port = output_port

	# Spawns a thread to handle server on
	def start_client_thread(self):

		# Create thread for client
		s = threading.Thread(target=self.run_client, args=(), daemon=True)

		# Spawn the thread
		s.start()

	# Method that accepts connections and send messages received to receiver
	def run_client(self):

		# Local server wait till someone connects to it
		print("Waiting for connection to server...")
		server = None

		# Attempt to connect for 15 seconds to server
		try:
			server = self.connect_to_server()
		except socket.timeout:
			print("No server connected within 15 seconds, restart program after exiting with ctrl + c")
			return
		except ConnectionRefusedError:
			print("Connection refused by server, restart program after exiting with ctrl + c")
			return

		print("Connection found: ", server.getpeername())

		# Set the recipient of sender
		self.input.set_recipient(server)
		self.running = True

		# Loops until stopped by main controller
		while self.running:

			# Get 128 byte buffer
			data = server.recv(128)
							
			# If not empty, assume it is valid data
			if ( data != b''):

				# Decode the data received
				decoded_data = data.decode()
				#print('Data: ', decoded_data)

				# Parse the data 
				parse_data(decoded_data, self.output_port)

		server.close()

	# Method that creates a socket and connects to server
	def connect_to_server(self):

		# Create a client socket with 15 second timeout
		client = socket.socket()
		#client.settimeout(15.0)
		client.connect((SERVER_IP, SERVER_PORT))

		return client

	