import mido 
import socket
import threading

from constant import LOCAL_IP, LOCAL_PORT
#from parsing import parse_data

# Class for creating a server socket that accepts multiple clients
class MultiServer:

	# Initialize stuff
	def __init__(self, output_port, input_obj):

		# Start server thread
		self.start_server_thread()
		self.running = False
		self.output_port = output_port
		self.input = input_obj

	# Spawns a thread to handle server on
	def start_server_thread(self):

		# Create server socket
		server = self.create_multi_server(LOCAL_IP, LOCAL_PORT)

		# Create thread for server
		s = threading.Thread(target=self.run_server, args=(server,), daemon=True)

		# Spawn the thread
		s.start()

	# Creates a socket server that listens for up to 5 connections
	def create_multi_server(self, ip_address, port):
		server = socket.socket()
		server.bind((ip_address, port))
		server.listen(5)

		return server

	# Method that is started on a new thread when new client connects
	def on_new_client(self, client, addr):

		# Add client to input recipient socket list
		self.input.add_recipient(client)

		# Loops until stopped by main controller
		try:
			while True:

				# Get 128 byte buffer
				data = client.recv(128)
								
				# If not empty, assume it is valid data
				if ( data != b''):

					# Send to all connected ports
					for recipient in self.input.recipients:
						recipient.send(data)

					# Decode the data received
					decoded_data = data.decode()
					#print('Data: ', decoded_data)
					print('Addr: ', addr, ' Data: ', decoded_data)

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
		except KeyboardInterrupt:
			print('done')

		# Remove client from input recipient socket list
		self.input.remove_recipient(client)			
		
		client.close()


	# Method that accepts connections and send messages received to receiver
	def run_server(self, server):

		# Local server wait till someone connects to it
		print("Waiting for connection to clients...")
		clientSocket = ''
		clientAddress = ''

		clientSocket, clientAddress = server.accept()
		print("New connection found: ", clientAddress)

		# Create thread for client
		s = threading.Thread(target=self.on_new_client, args=(clientSocket, clientAddress,), daemon=True)

				# Spawn the thread
		s.start()

		self.running = True

		while True:

			# Wait until a client connects to server
			try:
				# Wait for new connections
				clientSocket, clientAddress = server.accept()
				print("New connection found: ", clientAddress)

				# Create thread for client
				s = threading.Thread(target=self.on_new_client, args=(clientSocket, clientAddress,), daemon=True)

				# Spawn the thread
				s.start()

			except socket.timeout:
				print("Server timed out while waiting for clients, restart program after exiting with ctrl + c")
				server.close()
				return

		# Shut down server
		print('Shutting down multi server')
		server.shutdown(socket.SHUT_RDWR)
		server.close()

