import signal
import sys
from time import sleep
from convert import convert
import serial
import json
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 9876

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text\html')
        self.end_headers()
        out = get_last_serial()
        self.wfile.write(out)
        return


def signal_handler(signal,frame):
    #Gracefully shut down by closing serial port
    print('closing')
    ser.write('m 0\r')
    ser.close()
    server.socket.close()
    sys.exit(0)


def open_TM_serial(device_location):
    global ser
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
    # Wait for the command to take effect to be safe
    sleep(2)

    ser.flushInput()
    ser.flushOutput()


def get_last_serial():
    data = ser.readline()
    # Split off the TELEM part and convert
    return convert(data[8:])

# Any constants
device_location = '/dev/ttyACM0'

#Start things up
open_TM_serial(device_location)
#If we kill program then will close gracefully
signal.signal(signal.SIGINT, signal_handler)

server = HTTPServer(('',PORT_NUMBER),myHandler)
print 'Started server on port', PORT_NUMBER

server.serve_forever()
