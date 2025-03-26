import serial
ser = serial.Serial('COM3', 9600, timeout=1)  # Replace COMx with your port
ser.write(b'Test message\n')
ser.close()
