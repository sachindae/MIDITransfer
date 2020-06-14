# MIDITransfer
Project for peer-to-peer MIDI transfer

# Setup
1. Install mido and python-rtmidi using pip install  
2. Go to the project directory and run the following::

   python main.py -a
   
3. Set correct MIDI input/output ports as well as local IP in constant.py using the input printed to terminal
4. Setup port forwarding for your router with some unused port
5. Ask your friend to do 1-4 and set the server IP/port in constant.py

# Execution (python main.py)
- Run with no flags to run as client
- Run with -s flag to run as server
- Run with -a to print out ports and IPs
- Run with -d flag to print out ports
- Run with -l and or -p flags to print out local/public IP
