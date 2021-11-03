from typing import Tuple
from typing import Callable
from ordered_set import OrderedSet

"""
enum for states of the server. These are in-order!!! If another needs
to be set, set it in its appropriate order in the dictionary. All python
dictionaries are in order.
"""
state_enum = {'LISTENING': listening_validation,
              'READY': ready_validation,
              'CONFIRMING_FILENAME': fn_confirm_validation,
              'DIALOGING': dial_validation,
              'DONE': done_validation,
              'DESTROY_DATA': data_destroy_validation,
              'SAVE': save_validation}

"""
The functions are defined below
"""
def listening_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    if dgram == b'introduce':
        return True, 'ACK'
    else:
        retrun False, ''

def ready_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    if len(dgram) <= 255 and len(dgram) > 0:
        return True, dgram.decode()
    else:
        return False, ''

def fn_confirm_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    if dgram == b'correct':
        return True, '0'
    else:
        return False, ''

def dial_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    if len(dgram) == 100:
        sdgram = dgram.decode()
        try:
            current_packet_number = int(sdgram[:2])
            packet_length = int(sdgram[3:6])
            next_packet_number = int(dgram[-2:])
        except Error:
            print('\tDIAL: Error getting dgram packet index.')
        if state_struct.get_current_packet_number() + 1 != current_packet_number:
            return False, 'Packet out of order'
        if state_struct.get_next_packet_number() + 1 != next_packet_number:
            return False, 'Packet out of order'
        if packet_length + 7 != len(dgram):
            return False, 'Incomplete Packet'
        state_struct.set_current_packet_number(current_packet_number)
        state_struct.set_packet_length(packet_length)
        state_struct.set_next_packet_number(next_packet_number)
        state_struct.write_to_file(dgram)
    else:
        return False, ''
            

def done_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    
    pass

def data_destroy_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    pass

def save_validation(state_struct: JFTPState, dgram: bytes) -> bool, str:
    pass

"""
This class is used to organize the different states. They will be placed inside of a list and
sorted to be ordered of the enumeration. 

Having it organized this way allows there to be an ordered way to add more states and
to dictate their order of succession. 

The purpose of this class is to standardize a state and its transitions. 

It does not need to know the next state.
It does need to know its timeout counter.
It does need to know its timeout broadcasting.
It does need to know its validation.
It does need to know its validation broadcasting.
"""
class JFTPState:

    def __init__(self, enumeration: int, name: str,
                 validation: Callable[Tuple[bool, str]]
                 limit: int = 10):
        self._enum = enumeration
        self._limit = limit
        self._counter = 0
        self._timeout = False
        self._name = name
        self._validation = validation
        self._current_page_number
        self._packet_length
        self._next_page_number

    def set_current_page_number(self, page_num):
        self._current_page_number = page_num

    def set_packet_length(self, packet_len):
        self._packet_length

    def set_next_page_number(self, page_num):
        self._next_page_number

    def get_current_packet_number(self):
        return self._current_page_number

    def get_next_packet_number(self):
        return self._next_page_number

    def __str__(self):
        return self._name

    def __lt__(self, state: JFTPState):
        return self._enum < state.get_enum()

    def __eq__(self, state: JFTPState):
        return self._enum == state.get_enum()

    def __le__(self, state: JFTPState):
        return self._enum <= state.get_enum()

    def inc_counter(self):
        self._counter += 1

    def get_enum(self):
        return self._enum

    def validate(self, message: str) -> Tuple[bool, str]:
        return self.validation(message)

    def timeout(self):
        return self._timeout

    def reset_counter(self):
        self._counter = 0

reset_all(self):
        reset_counter()

        
def MAKE_CURRENT_STATES_LIST():
    state_set = StateSet()
    counter = 0
    for state, function in state_enum.items()
        state_set.add(JFTPState(counter, state, function))
        counter += 1

        
class StateSet:

    def __init__(self):
        self._set = OrderedSet()
        self._index = 0

    def insert_states(self, *state: JFTPState):
        l = list(state)
        self._set.add(l)

    def current_state(self) -> str:
        return str(_set[index])

    def reset_counters(self):
        for state in _set:
            state.reset_counter()

    def reset_counter(self):
        _set[_index].reset_counter()

    def check_timeout(self) -> bool:
        return self._set[index].timeout()

    def run_state(self, dgram):
        '''
        Need to use this method to run the different states. It delegates
        between the states and allows the state flow to change under this control.
        This is the engine of the state machine. 
        '''
        
        
        
