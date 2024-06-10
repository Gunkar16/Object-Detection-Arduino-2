import serial
import time

def is_device_connected(port):
    try:
        # Attempt to open the serial connection
        with serial.Serial(port) as ser:
            return True
    except serial.SerialException:
        # SerialException will be raised if the connection cannot be opened
        return False

# Define the serial port
port = 'COM13'  # replace with your specific port
baud_rate = 9600  # adjust according to your Arduino setup

try:
    # Create a serial connection object
    arduino = serial.Serial(port, baud_rate)

    # Continuous loop to read data and check connection status
    while True:
        # Check if device is connected
        if is_device_connected(port):
            print("Device is connected.")
            
            # Read data from Arduino
            data_from_arduino = arduino.readline().decode().strip()
            
            # Check if data is received
            if data_from_arduino:
                print("Data received from Arduino:", data_from_arduino)
        else:
            print("Device is not connected.")
        
        # Wait for a short duration before checking again

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    # Close the serial connection when program terminates
    if arduino.is_open:
        arduino.close()
        print("Serial connection closed.")
