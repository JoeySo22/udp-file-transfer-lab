#! /usr/bin/env python3

from socket import *
from select import select

# default params
serverAddr = ('localhost', 50000)       

import sys, re, os

def usage():
    print("usage: %s [--serverAddr host:port]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()

clientSocket = socket(AF_INET, SOCK_DGRAM)
filename = input("Input filename:")
file_o = None
file_fd = 0
sequence_num = 0
flags = b'00'
if os.path.exists(filename):
	# Open file
	file_o = open(filename, 'r')
	file_fd = file_o.fileno()
	#Start the arrays
	readSockets = [clientSocket]
	writeSockets = []
	expSockets = []
	
	#Should send first packet outside of select loop
	clientSocket.sendto(generate_bytes(), serverAddr)
	
	#Start the read write select loop
	while True:
		readReady, writeReady, expSockets = select.select(readSockets, 
			writeSockets, expSockets, 10)
		ack_flag = False
		for sock in readReady:
			message, server_port = sock.recvfrom(6)
			encoded_num = ''
			if sequence_num < 10:
				encoded_num = b'0' + str(sequence_num).encode()
			else:
				encoded_num = str(sequence_num).encode()
			ack_flag = (message == (b'ACK[' + 
				encoded_num + b']'))
	'''
	Another option is to see if perhaps we can just do a loop and block 
	the write by having read come first. This might suffice but we cannot
	figure out a way to timeout and to break timeout on an available socket.
	
	1. We might still be able to do the same functionality by having a flag
	of the correct response. How do we repeat a section?? << Don't worry
	about this for now. 
	'''
			
			
	
	#print(os.read(file_fd, 10))
	#file_o.close()
	pass
else:
	print('No such file: %s' % filename)

def generate_bytes():
	# We have to ecapsulate the bytes the reverse direction it is peeled. 
	# Its data, flags, sequence, and filename
	# Get the data
	data = os.read(file_fd, 68)
	# Get the length of data. If it is less than 68 then it is the end of the file
	if len(data) < 68:
		flags = b'99'
	# Add the flags
	data = flags + data
	# Add the sequence number
	seq_bytes = str(sequence_num).encode()
	if len(seq_bytes) < 2:
		seq_bytes = b'0' + seq_bytes
	data = seq_bytes + data
	# Add the filename
	data = filename.encode()
	return data
	

'''


clientSocket.sendto(message.encode(), serverAddr)
modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
print("Modified message from %s is <%s>" % (repr(serverAddrPort), modifiedMessage.decode()))
'''
