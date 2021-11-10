IP_ADDR_SIZE = 4
PORT_SIZE = 2
FILENAME_SIZE = 28
SEQUENCE_SIZE = 2
FLAGS_SIZE = 2
PACKET_SIZE = 100
DATA_SIZE = PACKET_SIZE - FLAGS_SIZE - SEQUENCE_SIZE - FILENAME_SIZE - PORT_SIZE
	- PORT_SIZE - IP_ADDR_SIZE # 60 w/ packet=100
	
class JFTPHeader:
	ip_addr: str = ''
	src_port: int = 0
	dest_port: int = 0
	filename: str = ''
	seq_current: int = 0
	flag_current: int = 0
	data: bytes = 0
	
	def __init__(self):
		pass
		
	def digest_application(self, data: bytes):
		pass
		
	

