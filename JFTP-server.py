#! /usr/bin/env python3
from socket import *
from select import select

from JFTP-states import *


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
"""
I must implement sequence numbers to enumerate the packets being sent.
I'm going to set a limit on the size of files able to be transmitted. I'm going
to go with 15MB like emails. Each packet will be size 999. So there might be
16 or so many packets. Maybe this may be enqueue'd to the front of the byte
array sent. So only 2 bytes are needed for the beginning and the end for the 
next packet. First 2 bytes are for id, last two bytes are for next. Going from
00 to 15

How do we know if we're done? Should I send what the total number of packets is 
supposed to be? Maybe it isn't as necessary and instead use the last 2 bytes to 
have a special meaning. The server won't have a special rule for knowing how 
large a file is to be transmitted. It will be up to the client to know the 15MB 
size. 
"""

current_state = LISTENING

readSockets = []
writeSockets = []
errorSockets = []

readSockets.append(serverSocket)
dgram = b''
client = None
filename = ''
file = None

state_set = MAKE_CURRENT_STATES_LIST()

while 1:
    # Select is mostly for utilizing the timeout as I understand. 
    readReady, writeReady, errorReady = select.select(readSockets, writeSockets,
                                                      errorSockets, 5) 
    print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
    # If the select timeout occurs, we need to increment the counter.
    if not readReady and not writeready and not errorReady:
        count_state()
        check_timeout()
    # If there is work to do, do it in here. 
    else:
        for sock in readReady:
            dgram, client = sock.recvfrom(999)
            print('dgram received from\t%s\t%s' % (client, dgram))
