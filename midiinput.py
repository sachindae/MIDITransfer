import mido 

from constant import MIDI_IN_PORT

# Class for handling midi input received by computer
class MIDIInput:

	# Initialize stuff
	def __init__(self):

		# Open input port that will be used and initialize recipient
		self.port = self.open_port(MIDI_IN_PORT)	
		self.recipient = None					

	# Method that listens for messages from input keyboard and sends to recipient
	def send_messages(self):

		# Blocking statement that listens for messages
		for msg in self.port:

			# Ignores aftertouch midi messages
			if msg.type in ('note_on', 'note_off'):

				# Press ctrl + c while sending a midi input signal to stop
				try:
					#print('Sent Msg: ', msg)

					# Sends MIDI message to the connected socket
					self.recipient.send(msg.hex().encode())
				except KeyboardInterrupt:
					break

	# Sets the recipient of the MIDI input
	def set_recipient(self, socket):
		self.recipient = socket

	# Closes this instances port
	def close_port(self):
		print('Input port closed: ', self.port.name)
		self.port.close()

	# Opens input port given the name and returns it
	def open_port(self, port_name):
		print('Input port opened: ', port_name)
		return mido.open_input(port_name)