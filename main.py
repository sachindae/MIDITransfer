import mido
import sys

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

		# Creates server or client
		if is_server:
			self.server = Server(self.output.port, input)
		else:
			self.client = Client(self.output.port, input)

	# Program loop
	def loop(self):

		# Loop till ctrl+c pressed
		try:

			while True:

				# Check for any new messages from input to send
				self.input.send_messages()

		except KeyboardInterrupt:

			# Stops the thread for server or client
			if self.server == None:
				self.client.running = False
			else:
				self.server.running = False

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
