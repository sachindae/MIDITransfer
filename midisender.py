import mido 
import socket

from constant import MIDI_IN_PORT, SERVER_IP, SERVER_PORT

# Class for handling midi input received by computer
class MIDISender:

	# Initialize stuff
	def __init__(self):
		print('init midi sender')

		# Print out all available midi ports
		# self.print_midi_ports()

		# Create a client socket with 15 second timeout
		client = socket.socket()
		client.settimeout(15)
		client.connect((SERVER_IP, PORT))

		# Open input port that will be used
		self.port = self.open_port(MIDI_IN_PORT)
		self.client = client

	# Method that listens for messages from input keyboard (non-blocking)
	def get_messages(self):
		for msg in self.port.iter_pending():
			print('Sender Msg: ', msg)
			self.client.send(msg.hex().encode())

	# Closes this instances port
	def close_port(self):
		print('input port closed: ', self.port.name)
		self.port.close()

	# Opens input port given the name and returns it
	def open_port(self, port_name):
		print('input port opened: ', port_name)
		return mido.open_input(port_name)

	# Prints available input ports out (use for testing)
	def print_midi_ports(self):
		print('available input ports')
		for port in mido.get_input_names():
			print(port)