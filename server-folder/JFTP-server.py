#! /usr/bin/env python3
from socket import *
import select

import os


# default params
serverAddr = ("", 50001)

import sys

verbose = False
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
	if '-v' in sys.argv:
		verbose = True
except:
    usage()

def pd(message):
	if not verbose:
		return
	print('[JFTP-SERVER] ' + message)

print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
print("ready to receive")

class JFTPSession:
	_client = None
	_debug = False
	FILENAME_SIZE = 28
	SEQUENCE_SIZE = 2
	FLAGS_SIZE = 2
	PACKET_SIZE = 100
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
		data = self.digest_header(data)
		if self._current_seq == 0:
			self._open_file = open(self._filename, 'w')
			self._fd = self._open_file.fileno()
		os.write(self._fd, data)
		if self._current_flag == 99:
			self._open_file.close()
			return 'FIN'
		return 'ACK' + str(self._current_seq), self._client
		
	#Only digest the header
	def digest_header(self, data:bytes):
		return self._get_flags(self._get_sequence(self._get_filename(data)))
		
	def _get_filename(self, data):
		#TODO: transform byte data into string. If sequence not 0 then confirm
		b = data[:self.FILENAME_SIZE]
		self._filename = ''.join([chr(_char) for _char in b if _char != 0])
		print(self._filename)
		return data[self.FILENAME_SIZE:]
		
	def _get_sequence(self, data):
		#TODO: transform byte data into integer. Check if it is the next packet
		self._current_seq = int(data[:self.SEQUENCE_SIZE].decode())
		return data[self.SEQUENCE_SIZE:]
	
	def _get_flags(self, data):
		#TODO: transform byte data into integer. Check if any important flags
		self._current_flag = int(data[:self.FLAGS_SIZE].decode())
		return data[self.FLAGS_SIZE:]


readSockets = []
writeSockets = []
errorSockets = []


print('serversocket = ')
print(serverSocket.getsockname())
readSockets.append(serverSocket)
writeSockets.append(serverSocket)
dgram = b''
client = None
client_list = []
session_dictionary: dict = {}
response_dict: dict = {}
timeout = 300 # 5 minutes for log when not serving

while 1:
	pd('entered select iteration')
	# Select is mostly for utilizing the timeout as I understand. 
	readReady, writeReady, errorReady = select.select(readSockets, writeSockets,
		errorSockets) 
	#print('select unblock')
	# If the select timeout occurs, we need to increment the counter.
	if not readReady and not writeReady and not errorReady:
		pd('timeout')
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
				print(dgram)
				# Set up the new session and a place for the response. 
				session_dictionary[client] = [JFTPSession(client), '']
				# Call the digestion and store the response to the dictionary.
				session_dictionary[client][1] = session_dictionary[client][0].digest_application(dgram)
			else:
				# Call the digestion and store the response to the dictionary.
				session_dictionary[client][1] = session_dictionary[client][0].digest_application(dgram)
				
		for sock in writeSockets:
			"""Each session has a response. For each socket, how do I know what I need
			to send back? Do I need another dictionary? """
			clients = session_dictionary.keys()
			clients_to_remove = []
			for client in clients:
				print(session_dictionary[client][1])
				response = session_dictionary[client][1]
				sock.sendto(response.encode(), client)
				#Delete the socket if it is finished.
				if response == 'FIN':
					clients_to_remove.append(client)
			for client in clients_to_remove:
				del session_dictionary[client]
