import mido
import socket

from midiinput import MIDIInput 
from midioutput import MIDIOutput 
from midisender import MIDISender 
from midireceiver import MIDIReceiver 

from constant import LOCAL_IP, SERVER_IP, PORT

# Main class used for running the program
class MidiTransfer:

	# Initialize the program
	def __init__(self):
		self.output = MIDIOutput()
		self.receiver = MIDIReceiver(self.output.port)
		self.sender = MIDISender()

	# Program loop
	def loop(self):

		# Loop till ctrl+c pressed
		try:

			while True:
				# Check for any new messages from input to send
				self.sender.get_messages()

		except KeyboardInterrupt:
			print('program closing')

			# Stops the receiver (server)
			self.receiver.running = False

			# Close MIDI ports after looping done
			self.sender.close_port()
			self.output.close_port()



# Start the program and loop it
if __name__ == "__main__":
	prog = MidiTransfer()
	prog.loop()
