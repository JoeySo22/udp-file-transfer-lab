from typing import Tuple
        
class JFTPProtocol:

    def __init__(self):
        self._set: list[str] = ['Listening', 'Handshaking', '']
        self._index: int = 0
        self._counter: int = 0
        self._limit: int = 10
        self._filename: str = ''
        self._file: file = None

    def current_state(self) -> str:
        return _set[_index]
        
    def give_message(self, message: bytes) -> bytes:
		if _current_state == 'Listening':
			return listening_handler(message)
		elif _current_state == 'Handshaking':
			handshaking_handler(message)
			
	def handshaking_handler(self, m:bytes) -> Tuple[bool, bytes]:
		if m == b''
	
	def listening_handler(self, m: bytes) -> bytes:
		if m == b'SYN':
			self._index += 1
			return b'SYN-ACK'
		return b''

    def reset_counter(self):
        self._counter = 0

    def check_timeout(self) -> bool:
        return self._set[index].timeout()

        
        
        
