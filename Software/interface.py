# interface.py

import comm

def read_register(ser,register_address):
    valW = comm.pack_32bit(register_address,0)
    comm.send_value(ser,valW)
    valR = comm.receive_value(ser)
    return (valR & 0x00FFFFFF)

def write_register(ser,register_address, value):
    valW = comm.pack_32bit(128+register_address,value)
    comm.send_value(ser,valW)
