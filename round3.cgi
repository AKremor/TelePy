#!/usr/bin/python
print "Content-Type: text/plain\n"

#initial serial connection setup
#import json
import serial
from convert import convert
import sqlite3
import time
#print time.strftime("%Y%m%d-%H%M%S")
db = sqlite3.connect(str(time.strftime("%Y%m%d-%H%M%S"))+'.db')
cursor = db.cursor()
cursor.execute('''
	CREATE TABLE packetdata(id INTEGER PRIMARY KEY, serial INTEGER,
				lat INTEGER, long INTEGER)
''')
db.commit()


#ser = serial.Serial('/dev/serial/by-id/usb-altusmetrum.org_TeleDongle-v0.2_000568-if00',115200,timeout=2)
def aconvert(data):
    data = "0504d43b0560b100202a58ea2a52ab560d070903231b0000000000000000000040abda"
    hex = [data[i:i+2] for i in range(0,len(data),2)]
    Serno = int(hex[1] + hex[0],16)
    cursor.execute('''INSERT INTO packetdata(serial,lat,long) VALUES (?,?,?)''',(Serno,Serno,Serno))
    db.commit()
    print Serno

#Tells the TeleDongle to start printing data packets
#ser.write('m 20\r')
run=False
while run == True:
    x = ser.readline()
    print(x)
#ser.close() #Close the serial connection nicely

cursor.execute('''SELECT id, serial, lat,long FROM packetdata''')
db.close()
#jsonarray = json.dumps(convert("0504d43b0560b100202a58ea2a52ab560d070903231b0000000000000000000040abda"))
#print jsonarray
print(convert("0504d43b0560b100202a58ea2a52ab560d070903231b0000000000000000000040abda"))
