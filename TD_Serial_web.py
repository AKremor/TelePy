import signal
import sys
from time import sleep, strftime
from convert import convert
import serial
from collections import deque
from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text\html')
        self.end_headers()
        self.wfile.write(convert(q.popleft()[8:]))
        return


def signal_handler(signal, frame):
    # Gracefully shut down by closing serial port and web server
    print('KeyboardInterrupt, shutting down')
    ser.write('m 0\r')
    ser.close()
    file.close()
    server.socket.close()
    sys.exit(0)


def open_TM_serial(location):
    global ser

    ser = serial.Serial(location, 115200)

    if ser.isOpen():
        print('Serial connection opened')
    else:
        print('Serial connection failed')
        sys.exit(0)

    # Throw away any old data
    ser.flushInput()
    ser.flushOutput()

    # Get TD to output packets
    ser.write('m 20\r')
    # Wait for the command to take effect to be safe
    sleep(2)

    ser.flushInput()
    ser.flushOutput()


def serial_read(q):
    while True:
        recent_packet = ser.readline()
        q.appendleft(recent_packet)
        file.write(recent_packet)
        print(recent_packet)


def save_to_file():
    filename = str(strftime("%Y%m%d-%H%M%S")) + '.txt'
    global file
    file = open(filename, 'w')
    print('Logging to {0}'.format(filename))


# Any constants
PORT_NUMBER = 9876

# If serial connection fails try other line, can find location with dmesg
location = '/dev/serial/by-id/usb-altusmetrum.org_TeleDongle-v0.2_000568-if00'
# location = '/dev/ttyACM0'

# If we kill program, close gracefully
signal.signal(signal.SIGINT, signal_handler)

open_TM_serial(location)

save_to_file()

server = HTTPServer(('', PORT_NUMBER), myHandler)
print('Started server on port {0}\n'.format(PORT_NUMBER))

q = deque(maxlen=100)
# Run serial_read in its own thread
t = Thread(target=serial_read, args=(q,))
t.daemon = True
t.start()

server.serve_forever()
