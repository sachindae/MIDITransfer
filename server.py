import mido 
import socket
import threading

from constant import LOCAL_IP, LOCAL_PORT, SERVER_IP, SERVER_PORT

# Class for creating a server socket
class Server:

	# Initialize stuff
	def __init__(self, output_port, input):
		#print('init server')

		# Start server thread
		self.start_server_thread()
		self.running = True
		self.output_port = output_port
		self.input = input

	# Spawns a thread to handle server on
	def start_server_thread(self):

		# Create server socket
		server = self.create_server(LOCAL_IP, LOCAL_PORT)

		# Create thread for server
		s = threading.Thread(target=self.run_server, args=(server,), daemon=True)

		# Spawn the thread
		s.start()

	# Creates a socket server and return it
	def create_server(self, ip_address, port):
		server = socket.socket()
		server.bind((ip_address, port))
		server.listen()
		server.settimeout(15.0)

		return server

	# Method that accepts connections and send messages received to receiver
	def run_server(self, server):

		# Local server wait till someone connects to it
		print("Waiting for connection to client...")
		clientSocket = ''
		clientAddress = ''

		# Accept connections for 15 seconds
		try:
			clientSocket, clientAddress = server.accept()
		except socket.timeout:
			print("No client connected within 15 seconds, restart program after exiting with ctrl + c")
			server.close()
			return

		print("Connection found: ", clientAddress)

		# Set the recipient of sender
		self.input.set_recipient(clientSocket)

		# Loops until stopped by main class
		while self.running:

			# Get 128 byte buffer
			data = clientSocket.recv(128)
							
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

		print('Shutting down server')
		server.shutdown(socket.SHUT_RDWR)
		server.close()
