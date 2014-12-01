import signal
import sys
from time import sleep
from convert import convert
import serial
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text\html')
        self.end_headers()
        out = get_last_serial()
        self.wfile.write(out)
        return


def signal_handler(signal,frame):
    # Gracefully shut down by closing serial port and web server
    print('KeyboardInterrupt, shutting down')
    ser.write('m 0\r')
    ser.close()
    server.socket.close()
    sys.exit(0)


def open_TM_serial(second_location):
    global ser
    first_location = '/dev/serial/by-id/usb-altusmetrum.org_TeleDongle-v0.2_000568-if00'

    try:
        ser = serial.Serial(first_location, 115200)
    # Check what the actual exception is
    except serial.SerialException:
        print('Auto detect fail, attempt connection with manual location')
        try:
            ser = serial.Serial(second_location, 115200)
        except:
            print('Cannot connect with either location')

    if ser.isOpen():
        print('Serial connection open')
    else:
        print('Serial connection fail')
        sys.exit(0)

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
    # Split off the 'TELEM 22' part and convert
    return convert(data[8:])

# Any constants
PORT_NUMBER = 9876

# Only set this if auto-detect failing
# Unplug then plug in TeleDonge, then run dmesg to get location
second_location = '/dev/ttyACM0'

# Open up the serial connection to TM
open_TM_serial(device_location)
# If we kill program then will close gracefully
signal.signal(signal.SIGINT, signal_handler)

server = HTTPServer(('',PORT_NUMBER),myHandler)
print 'Started server on port', PORT_NUMBER

server.serve_forever()
