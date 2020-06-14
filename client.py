import mido 
import socket
import threading

from constant import SERVER_IP, SERVER_PORT
#from parsing import parse_data

# Class for creating a client socket
class Client:

	# Initialize stuff
	def __init__(self, output_port, input_obj):

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

		# 
		print("Waiting for connection to server...")
		server = None

		# Attempt to connect to server
		try:
			server = self.connect_to_server()
		except socket.timeout:
			print("Server connection attempt timed out, restart program after exiting with ctrl + c")
			return
		except ConnectionRefusedError:
			print("Connection refused by server, restart program after exiting with ctrl + c")
			return
		except KeyboardInterrupt:
			return

		print("Connection found: ", server.getpeername())

		# Set the recipient socket of input
		self.input.set_recipient(server)
		self.running = True

		# Loops until stopped by main controller
		while self.running:

			try:
				# Get 128 byte buffer
				data = server.recv(128)
								
				# If not empty, assume it is valid data
				if ( data != b''):

					# Decode the data received
					decoded_data = data.decode()
					#print('Data: ', decoded_data)

					# Parse the data 
					#parse_data(decoded_data, self.output_port)

					endIdx = 0
					msgNum = 0

					# Parse each note in data
					while ( endIdx < len(data) ):

						startIdx = (msgNum) * 8
						endIdx = startIdx + 8

						msg = mido.Message.from_hex(decoded_data[startIdx:endIdx])
						self.output_port.send(msg)

						print("Received Msg: ", msg)

						msgNum += 1
						endIdx += 1

			except ConnectionResetError:
				print('Server closed, program ending press ctrl + c')
				break

		server.close()

	# Method that creates a socket and connects to server
	def connect_to_server(self):

		# Create a socket and connect it to server
		client = socket.socket()
		client.connect((SERVER_IP, SERVER_PORT))

		return client

	