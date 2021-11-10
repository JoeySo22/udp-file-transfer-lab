#! /usr/bin/env python3
from socket import *
from select import select

import os


# default params
serverAddr = ("", 50001)

import sys
def usage():
    print("usage: %s [--serverPort <port>]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverPort":
            serverAddr = ("", int(args[0])); del args[0]
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()

print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
print("ready to receive")

readSockets = []
writeSockets = []
errorSockets = []

readSockets.append(serverSocket)
dgram = b''
client = None
session_dictionary: dict = {}

while 1:
    # Select is mostly for utilizing the timeout as I understand. 
    readReady, writeReady, errorReady = select.select(readSockets, writeSockets,
                                                      errorSockets, 5) 
    print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
    # If the select timeout occurs, we need to increment the counter.
    if not readReady and not writeready and not errorReady:
        pass #TODO: fill in for nothing
    # If there is work to do, do it in here. 
    else:
        for sock in readReady:
            dgram, client = sock.recvfrom(100)
            print('dgram received from\t%s\t%s' % (client, dgram))
            #the client received is also a random port number which we should 
            #reply
            if client not in session_dictionary:
				session_dictionary[client] = JFTPSession(client)
				session_dictionary[client].digest_application(dgram)
			else:
				session_dictionary[client].digest_application(dgram)
            
class JFTPSession:
	_client = None
	_debug = False
	FILENAME_SIZE = 28
	SEQUENCE_SIZE = 2
	FLAGS_SIZE = 2
	PACKET_SIZE = 100
	DATA_SIZE = FLAGS_SIZE - SEQUENCE_SIZE - FILENAME_SIZE - IP_ADDR_SIZE
	_filename = ''
	_open_file = None
	_fd = -1
	_current_seq = 0
	_current_flag = 0
	
	def __init__(self, client, debug=False):
		self._client = client
		self._debug = debug
	
	#Only digest the data
	def digest_application(self, data) -> str:
		data = digest_header(data)
		if _current_seq is 0:
			_open_file = open(_filename, 'w')
			_fd = _open_file.fileno()
		os.write(_fd, data)
		if _current_flag is 99:
			_open_file.close()
			return 'FIN'
		return 'ACK' + str(_current_seq)
		
	#Only digest the header
	def digest_header(self, data:bytes):
		return _get_flags(_get_sequence(_get_filename(data)))
		
	def _get_filename(self, data):
		#TODO: transform byte data into string. If sequence not 0 then confirm
		return data[:FILENAME_SIZE]
		
	def _get_sequence(self, data):
		#TODO: transform byte data into integer. Check if it is the next packet
		return data[:SEQUENCE_SIZE]
	
	def _get_flags(self, data):
		#TODO: transform byte data into integer. Check if any important flags
		return data[:FLAGS_SIZE]
		
	
