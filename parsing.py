import mido

from multiprocessing import Pool

# Method that creates MIDI msg from 8 bytes and send to output
def create_and_output(data, output_port):
	# Send message received to output port
	msg = mido.Message.from_hex(data)
	output_port.send(msg)

def chunks(lst, n):
    # Returns chunks of size n
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Method that parses data into MIDI messages
def parse_data(data, output_port):
	#print('name: ', output_port.name)
	#msgs = chunks(data, 8)

	#for m in msgs:
	#	create_and_output(m, output_port)

	#with Pool() as p:
	#	for m in msgs:
	#		p.apply_async(create_and_output, args=(m, output_port,))

	endIdx = 0
	msgNum = 0

	# Parse each note in data
	while ( endIdx < len(data) ):

		startIdx = (msgNum) * 8
		endIdx = startIdx + 8

		msg = mido.Message.from_hex(data[startIdx:endIdx])
		output_port.send(msg)

		#print("Receiver Msg: ", msg)

		msgNum += 1
		endIdx += 1