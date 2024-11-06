import serial
import keyboard
import time

# Open a serial connection with the specified port and baud rate
def init_ser_port(port='COM8', baudrate=9600):
    """
    Args:
    - port (str): The COM port for the serial connection (e.g., 'COM8' or '/dev/ttyUSB0').
    - baudrate (int): Baud rate for the serial connection.
    
    Returns:
    - ser (serial.Serial): The serial connection object if successful, otherwise None.
    """
    try:                                                                        # Initialize serial connection
        ser = serial.Serial(port, baudrate, timeout=0.1)
        print(f"Serial connection opened on {port} with baudrate {baudrate}")
        return ser
    
    except serial.SerialException as e:                                         # Handle error if the serial port fails to open
        print(f"Error opening serial connection: {e}")
        return None

# Monitor for integer keypress and send the value to serial connection and check for immeadiate response
def send_value(ser):
    """    
    Args:
    - ser (serial.Serial): The serial connection object.
    """
    print("Press an integer key (0-9) to send the value over serial. Press 'q' to quit.")
    
    while True:                                                         # Continuous loop to monitor for keypress events
        for i in range(10):                                             # Loop over each integer key to check for press
            if keyboard.is_pressed(str(i)):
                ser.write(str(i).encode())                              # Send the pressed integer as a byte over serial
                print(f"Sent: {i}")

                time.sleep(0.1)
                receive_value(ser)                                      # Call receive_value to check if there’s an incoming response
                time.sleep(0.2)
        
        if keyboard.is_pressed('q'):                                    # Check if the 'q' key is pressed to exit the loop
            print("Exiting...")
            break

# Check for and reads any incoming data from the serial connection, then prints it.
def receive_value(ser):
    """    
    Args:
    - ser (serial.Serial): The serial connection object.
    """
    if ser.in_waiting > 0:                                  # Check if there is data waiting in the serial buffer
        received_data = ser.readline().decode().strip()     # Decode data read to a string, and strip whitespace
        print(f"Received: {received_data}")


ser = init_ser_port(port='COM8', baudrate=9600)     # Open serial connection

if ser:                 # Proceed if the serial connection was successfully opened
    send_value(ser)     # Start monitoring for keypresses and sending values over serial
    ser.close()         # Close the serial connection when done
