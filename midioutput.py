import mido # library for reading midi
import time # for sleeping

from constant import MIDI_OUT_PORT

# Class for handling midi output 
class MIDIOutput:

	# Initialize stuff
	def __init__(self):

		# Open output port that will be used
		self.port = self.open_port(MIDI_OUT_PORT)

		# Output a welcome message to verify its working
		self.welcome_message()

	# Closes this instances port
	def close_port(self):
		print('Output port closed: ', self.port.name)
		self.port.close()

	# Opens output port given the name and returns it
	def open_port(self, port_name):
		print('Output port opened: ', port_name)
		return mido.open_output(port_name, autoreset=True)

	# Sends a chord to output as a test for 2 seconds
	def welcome_message(self):
		# Create messages
		msg1 = mido.Message('note_on', channel=2, note=65, velocity=64, time=6.2)
		msg2 = mido.Message('note_on', channel=2, note=71, velocity=64, time=6.2)
		msg3 = mido.Message('note_on', channel=2, note=75, velocity=64, time=6.2)
		msg4 = mido.Message('note_on', channel=2, note=55, velocity=64, time=6.2)

		# Send messages to port
		self.port.send(msg1)
		self.port.send(msg2)
		self.port.send(msg3)
		self.port.send(msg4)

		# Hold down notes for 2 secs
		time.sleep(2)

		# Turn em off by just resetting the port
		self.port.reset()