import sys

from midioutput import MIDIOutput 
from midiinput import MIDIInput 
from server import Server 
from client import Client 

from multimidiinput import MultiMIDIInput
from multiserver import MultiServer

from information import print_ports, print_local_ip, print_public_ip, print_all
	
# Main class used for running the program
class MidiTransfer:

	# Initialize the program
	def __init__(self, is_server, is_multi):

		# Check if need to send input to multiple or just one socket
		if is_multi:
			self.input = MultiMIDIInput()	# Opens multi input port
		else:
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

			# Start sending MIDI whenever received from input (blocking)
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


# Start the program and loop it
if __name__ == "__main__":

	# Parse cmd line args (-s for server, -d for display ports)
	is_server = '-s' in sys.argv
	is_multi = '-m' in sys.argv
	display_ports = '-d' in sys.argv
	display_local_ip = '-l' in sys.argv
	display_public_ip = '-p' in sys.argv
	display_all = '-a' in sys.argv

	# Checks flags
	if display_all:

		# Displays all information needed (ports, ips)
		print_all()

	elif display_ports:

		# Display MIDI ports available in console
		print_ports()

	elif display_local_ip or display_public_ip:

		print()

		# Display your computers IP
		if display_local_ip:
			print_local_ip()

		# Display your routers IP
		if display_public_ip:
			print_public_ip()

		print()

	else:
		print()

		# Start the program
		prog = MidiTransfer(is_server, is_multi)
		prog.loop()

		print()
