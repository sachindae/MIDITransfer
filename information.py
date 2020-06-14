import mido
import socket
import urllib.request

# Method that prints out MIDI input/output ports
def print_ports():
	# Print input ports
	print('\nAvailable input ports')
	print('---------------------')
	for port in mido.get_input_names():
		print(port)

	# Print output ports
	print('\nAvailable output ports')
	print('---------------------')
	for port in mido.get_output_names():
		print(port)
	print()

# Method that prints out your computers IP (local IP)
def print_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	print('Local IP Address:', s.getsockname()[0])
	s.close()

# Method that prints out your routers IP (public IP)
def print_public_ip():
	external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
	print('Public IP Address:', external_ip)

# Method that prints out all the information
def print_all():
	# Displays all information needed (ports, ips)
	print_ports()

	print('IP Addresses')
	print('------------')

	# Display your computers IP
	print_local_ip()

	# Display your routers IP
	print_public_ip()

	print()