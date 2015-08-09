import signal
import sys
from time import sleep
from convert import convert
import serial
import json

def signal_handler(signal,frame):
        #Gracefully shut down by closing serial port
        print('closing')
        ser.write('m 0\r')
        ser.close()
        sys.exit(0)


#Any constants
device_location = '/dev/ttyACM0'

ser = serial.Serial(device_location, 115200)
if ser.isOpen():
        print('Serial connection open')
else:
        print('Serial connection fail')

#Throw away any old data
ser.flushInput()
ser.flushOutput()

#Get TD to output packets
ser.write('m 20\r')
#Wait for the command to take effect to be safe
sleep(2)

ser.flushInput()
ser.flushOutput()

#If we kill program then will close gracefully
signal.signal(signal.SIGINT, signal_handler)

for i in range(1,200):
        data = ser.readline()
        #Split off the TELEM part
        data = data.split(' ')[1]
        print(convert(data))

ser.write('m 0\r')
ser.close()
