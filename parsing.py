import mido

# Method that parses data into MIDI messages
def parse_data(data, output_port):
	msgNum = 0
	endIdx = 0

	# Parse each note in data
	while ( endIdx < len(data) ):

		startIdx = (msgNum) * 8
		endIdx = startIdx + 8

		# If aftertouch message is received, skip for now
		if (data[startIdx] == 'D'):
			break

		# Send message received to output port
		msg = mido.Message.from_hex(' ' + data[startIdx:endIdx])
		output_port.send(msg)

		print("Receiver Msg: ", msg)

		msgNum += 1
		endIdx += 1