import serial
import keyboard
import time
import numpy as np
import struct

# Open a serial connection with the specified port and baud rate
def init_ser_port(port='COM8', baudrate=9600):
    """
    Args:
    - port (str): The COM port for the serial connection
    - baudrate (int): Baud rate for the serial connection
    
    Returns:
    - ser (serial.Serial): The serial connection object if successful, otherwise None
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=0.1)                            # Attempt to open the serial connection
        print(f"Serial connection opened on {port} with baudrate {baudrate}")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial connection: {e}")                              # Print an error message if the connection fails
        return None

# Pack a 32-bit data: first 8 bits for the address, last 24 bits for data
def pack_32bit(address, data):
    """
    Args:
    - address (int): 8-bit address (0-255)
    - data (int): 24-bit data (0-16777215)
    
    Returns:
    - bytes: Packed 32-bit value as a byte array
    """
    if not (0 <= address <= 255):                                       # Validate the address is within 8-bit range
        raise ValueError("Address must be an 8-bit value (0-255).")
    if not (0 <= data <= 16777215):                                     # Validate the data is within 24-bit range
        raise ValueError(f"Data must be a 24-bit value (0-16777215). {data}")
    
    value = (address << 24) | data                                      # Combine the address and data into a single 32-bit integer
    return value.to_bytes(4, 'little')                                  # Convert the 32-bit value into a 4-byte array in little-endian order

# Unpack the received 32-bit data into address and data
def unpack_32bit(data_bytes):
    """
    Args:
    - data_bytes (bytes): 4-byte array representing 32-bit packed data
    
    Returns:
    - tuple (address, data): where address is 8 bits and data is 24 bits
    """
    if len(data_bytes) != 4:                                # Ensure the received data is 4 bytes
        raise ValueError("Data must be 4 bytes long.")
    
    value = int.from_bytes(data_bytes, 'little')            # Convert the 4-byte array into a 32-bit integer
    address = (value >> 24) & 0xFF                          # Extract the 8-bit address from the most significant byte
    data = value & 0xFFFFFF                                 # Extract the 24-bit data from the least significant 3 bytes
    return address, data

# Send 32-bit values over serial
def send_value(ser, data):
    """
    Args:
    - ser (serial.Serial): The serial connection object
    """
    ser.write(data)                              # Send the packed data over the serial connection    
    time.sleep(0.1)                              # Time delay to allow for data transmission

# Function to receive and unpack 32-bit data from the serial connection
def receive_value(ser):
    """
    Non-blocking function to receive data from STM32.
    
    Args:
    - ser (serial.Serial): The serial connection object.
    
    Returns:
    - int: The 24-bit received data, or None if no data is available.
    """
    if ser.in_waiting >= 4:  # Only read if at least 4 bytes are available
        data_bytes = ser.read(4)
        # _, data = unpack_32bit(data_bytes)  # Unpack received data
        return data_bytes

    return None  # No data available yet

def receive_samples(ser, adc_num, buffer_size):
    """
    Non-blocking function to receive and unpack 12-bit ADC samples from STM32.
    
    Args:
    - ser (serial.Serial): The serial connection object.
    - buffer_size (int): Number of bytes to read.

    Returns:
    - np.ndarray: An array of 12-bit ADC samples, or None if no data is available.
    """
    send_value(ser,pack_32bit(99+adc_num,0))
    if ser.in_waiting >= buffer_size:  # Read only if enough data is available
        data_bytes = ser.read(buffer_size)  # Read buffer_size bytes
        samples = np.frombuffer(data_bytes, dtype=np.uint16)  # Convert bytes to 16-bit integers
        
        # Since STM32 packs 12-bit ADC values into 16-bit containers, mask out the higher bits
        samples = samples & 0x0FFF  # Extract only the lower 12 bits
        
        return samples[8:]

    return None  # No data available yet
