import mido
import sys
import time

from midioutput import MIDIOutput 
from midiinput import MIDIInput 
from server import Server 
from client import Client 

# Main class used for running the program
class MidiTransfer:

	# Initialize the program
	def __init__(self, is_server):

		self.input = MIDIInput()		# Opens input port
		self.output = MIDIOutput()		# Opens output port
		self.server = None				# Init value
		self.client = None				# Init value
		self.is_server = is_server		# Server or client

		# Creates server or client
		if is_server:
			self.server = Server(self.output.port, self.input)
		else:
			self.client = Client(self.output.port, self.input)

	# Program loop
	def loop(self):

		# Loop till ctrl+c pressed
		try:

			# Wait till server or client are running
			if self.is_server:
				while not self.server.running:
					continue
			else:
				while not self.client.running:
					continue

			#while True:
				#time.sleep(5)

			# Start sending MIDI whenever received from input
			self.input.send_messages()

		except KeyboardInterrupt:

			# Stops the thread for server or client
			if self.is_server:
				self.server.running = False
			else:
				self.client.running = False

			# Close MIDI ports after looping done
			self.input.close_port()
			self.output.close_port()

# Method that prints out MIDI input/output ports
def print_ports():
	# Print input ports
	print('\navailable input ports')
	print('---------------------')
	for port in mido.get_input_names():
		print(port)

	# Print output ports
	print('\navailable output ports')
	print('---------------------')
	for port in mido.get_output_names():
		print(port)
	print()

# Start the program and loop it
if __name__ == "__main__":

	# Parse cmd line args (-s for server, -d for display ports)
	is_server = '-s' in sys.argv
	display_ports = '-d' in sys.argv

	# Display ports or execute
	if display_ports:

		# Display MIDI ports available in console
		print_ports()

	else:
		print()

		# Start the program
		prog = MidiTransfer(is_server)
		prog.loop()

		print()
