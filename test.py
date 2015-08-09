__author__ = 'Anthony'
from convert import convert, byte_unpacker, verify_packet

with open('test.telem', 'rb') as myfile:
    test_packets = myfile.readlines()

for packet in test_packets:
    data = packet.split(' ')[1]
    #print data

    try:
        print convert(data)
        print verify_packet(data)
    except IOError:
        print data

