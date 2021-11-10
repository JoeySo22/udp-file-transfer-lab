from typing import Tuple
        
class JFTPProtocol:

    def __init__(self):
        self._set: list[str] = ['LISTENING', 'HANDSHAKING', 'READY', 
			'TRANSFERING', 'SAVING', 'CLEANING']
        self._index: int = 0
        self._counter: int = 0
        self._limit: int = 10
        self._filename: str = ''
        self._file: file = None

    def current_state(self) -> str:
        return _set[_index]
        
    def give_message(self, message: bytes) -> bytes:
		if _current_state == 'LISTENING':
			return listening_handler(message)
		elif _current_state == 'HANDSHAKING':
			return handshaking_handler(message)
		elif _current_state == 'READY':
			return ready_handler(message)
		elif _current_state == 'TRANSFERING':
			return transfering_handler(message)
		elif _current_state == 'SAVING':
			return saving_handler(message)
		elif _current_state == 'CLEANING':
			return cleaning_handler(message)
			
	def ready_handler(self, m: bytes) -> bytes:
		
			
	def handshaking_handler(self, m: bytes) -> bytes:
		if m == b'':
			self._counter += 1
			check_timeout()
		elif m == b'ACK':
			
	
	def listening_handler(self, m: bytes) -> bytes:
		if m == b'SYN':			# Good
			self._index += 1
			return b'SYN-ACK'
		elif m == b'':
			self._counter += 1
			check_timeout()
		return b''

    def reset_counter(self):
        self._counter = 0

    def check_timeout(self) -> bool:
        return _counter >= _limit

        
        
        
