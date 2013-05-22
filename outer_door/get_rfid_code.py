import serial
ser = serial.Serial('/dev/ttyUSB0', 2400, timeout=120)
string = ser.read(12)
string = string[2:]
print string.strip()

