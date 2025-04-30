import serial
import time


def serial_data_output():
    return [1,2,3,4,5,6,7]

# Replace '/dev/ttyUSB0' with your actual port
port = '/dev/ttyUSB0'  # or '/dev/ttyACM0'
baud_rate = 921600

# Initialize serial connection
ser = serial.Serial(port, baud_rate, timeout=1)

try:
    time.sleep(2)  # Wait for the connection to initialize
    
    
    measure_cnt = 0
    while True:
        if measure_cnt > 1000:
            break
        #if ser.in_waiting > 0:
        # Send the message

        start_measure_message = bytes(0xA1)
        # print(f"Sent: {start_measure_message.hex()}") 
        ser.write(start_measure_message) #.encode('utf-8'))  # Encode the string to bytes
        
        response = ser.read(ser.in_waiting).decode('utf-8').rstrip()
        if ser.in_waiting > 0:
            data = ser.readline() #.decode('utf-8').rstrip()  # Read a line of data
            print(f"Received: {data.hex()}")

        measure_cnt += 1
    
    # end_measure_message = "iHALT"
    # ser.write(end_measure_message.encode('utf-8'))  # Encode the string to bytes
    
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()