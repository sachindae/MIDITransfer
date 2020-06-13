import mido 
import socket
import threading

from constant import LOCAL_IP, LOCAL_PORT, SERVER_IP, SERVER_PORT

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

		# Loops until stopped by main class
		while self.running:

			# Get 128 byte buffer
			data = server.recv(128)
							
			# If not empty, assume its a legit message
			if ( data != b''):

				# Decode msg
				dec = data.decode()
				print('Data: ', dec)
		
				msgNum = 0
				endIdx = 0

				# Parse each note in data
				while ( endIdx < len(dec) ):

					startIdx = (msgNum) * 8
					endIdx = startIdx + 8

					# If aftertouch message is received, skip for now
					if (dec[startIdx] == 'D'):
						break

					# Send message received to output port
					msg = mido.Message.from_hex(' ' + dec[startIdx:endIdx])
					self.output_port.send(msg)

					print("Receiver Msg: ", msg)

					msgNum += 1
					endIdx += 1

		server.shutdown()
		server.close()

	# Method that creates a socket and connects to server
	def connect_to_server(self):

		# Create a client socket with 15 second timeout
		client = socket.socket()
		client.settimeout(15)
		client.connect((SERVER_IP, SERVER_PORT))

		return client
