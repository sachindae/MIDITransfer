import mido

from multiprocessing import Pool

outputport = None

# Method that creates MIDI msg from 8 bytes and send to output
def create_and_output(data):
	# Send message received to output port
	msg = mido.Message.from_hex(data)
	outputport.send(msg)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Method that parses data into MIDI messages
def parse_data(data, output_port):
	msgs = chunks(data, 8)
	outputport = output_port

	with Pool(5) as p:
		p.map(create_and_output, msgs)

	# Parse each note in data
	#while ( endIdx < len(data) ):

		#startIdx = (msgNum) * 8
		#endIdx = startIdx + 8

		

		#print("Receiver Msg: ", msg)

		#msgNum += 1
		#endIdx += 1