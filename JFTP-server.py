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
client_list = []
session_dictionary: dict = {}
response_dict: dict = {}
timeout = 300 # 5 minutes for log when not serving

while 1:
    # Select is mostly for utilizing the timeout as I understand. 
    readReady, writeReady, errorReady = select.select(readSockets, writeSockets,
                                                      errorSockets, timeout) 
    print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
    # If the select timeout occurs, we need to increment the counter.
    if not readReady and not writeready and not errorReady:
        timeout = 300
    # If there is work to do, do it in here. 
    else:
		# ensure that the timeout is only 10 seconds because it is working
		timeout = 10 
        for sock in readReady:
            dgram, client = sock.recvfrom(100)
            print('dgram received from\t%s\t%s' % (client, dgram))
            """The client received is also a random port number which we should 
            reply."""
            session_response: str = ''
            if client not in session_dictionary:
				# Set up the new session and a place for the response. 
				session_dictionary[client] = (JFTPSession(client), '')
				# Create a new socket for sending
				new_write_socket = socket(AF_NET, SOCK_DRGRAM)
				new_write_socket.bind(client)
				# Add the new socket to the list for select
				writeSockets.append(new_write_socket)
				# Call the digestion and store the response to the dictionary.
				session_dictionary[client][1] = 
					session_dictionary[client].digest_application(dgram)
			else:
				# Call the digestion and store the response to the dictionary.
				session_dictionary[client][1] = 
					session_dictionary[client].digest_application(dgram)
				
		for sock in writeSockets:
			"""Each session has a response. For each socket, how do I know what I need
			to send back? Do I need another dictionary? """
			sock_host, sock_port = sock.getpeername()
			response = session_dictionary[(socket_host, sock_port)][1]
			sock.send(response)
			#Delete the socket if it is finished.
			if response == 'FIN':
				writeSockets.remove(sock)
            
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
			return 'FINACK', self._client
		return 'ACK' + str(_current_seq), self._client
		
	#Only digest the header
	def digest_header(self, data:bytes):
		return _get_flags(_get_sequence(_get_filename(data)))
		
	def _get_filename(self, data):
		#TODO: transform byte data into string. If sequence not 0 then confirm
		_filename = data[:FILENAME_SIZE].decode()
		return data[FILENAME_SIZE:]
		
	def _get_sequence(self, data):
		#TODO: transform byte data into integer. Check if it is the next packet
		_current_seq = int(data[:SEQUENCE_SIZE].decode())
		return data[SEQUENCE_SIZE:]
	
	def _get_flags(self, data):
		#TODO: transform byte data into integer. Check if any important flags
		_current_flag = int(data[:FLAGS_SIZE].decode())
		return data[FLAGS_SIZE:]
		
	
