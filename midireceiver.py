import mido 
import socket
import threading

from constant import LOCAL_IP, LOCAL_PORT

# Class for handling midi input received over network (aka sets up server and listens)
class MIDIReceiver:

	# Initialize stuff
	def __init__(self, output_port):
		print('init midi receiver')

		self.running = True

		# Create server that ppl connect to
		server = self.create_server(LOCAL_IP, LOCAL_PORT)

		# Create thread for server
		s = threading.Thread(target=self.run_server, args=(server, output_port), daemon=True)

		# Spawn the thread
		s.start()

	# Creates a socket server and return it
	def create_server(self, ip_address, port):
		server = socket.socket()
		server.bind((ip_address, port))
		server.listen()

		return server

	# Method that accepts connections and send messages received to midi output
	def run_server(self, server, output_port):

		# Local server wait till someone connects to it
		print("Waiting for connection")
		clientSocket, clientAddress = server.accept()
		print("Connection found: ", clientAddress)

		# Loops until stopped by main class
		while self.running:

			# Get 256 byte buffer
			data = clientSocket.recv(1024)
							
			# If not empty, assume its a legit message
			if ( data != b''):
				# Decode msg
				dec = data.decode()
				print('Data: ', dec)
		
				msgNum = 0
				endIdx = 0
				msg = ''

				# Parse each note in data
				while ( endIdx <= len(dec) ):

					startIdx = (msgNum) * 8
					endIdx = startIdx + 8
					#print('s: ', startIdx, 'e: ', endIdx)

					#print("SLICE ", msgNum, ": ", dec[startIdx:endIdx])
					if (dec[startIdx] == 'D'):
						break
					msg = mido.Message.from_hex(' ' + dec[startIdx:endIdx])

					print("Receiver Msg: ", msg)
					output_port.send(msg)
					msgNum += 1
					endIdx += 1

		server.shutdown()
		server.close()
