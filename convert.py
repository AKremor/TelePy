def signedhex(num):
    intval = int(num,16)
    if intval >=2147483648 :
        intval -= 2147483648
    return intval

import struct
def convert(packet):
    converted={}
    hex = [packet[i:i+2] for i in range(0,len(packet),2)]
    
    #append serial number to list
    converted['serno'] = int(hex[1] + hex[0],16)
    #Append Tick to list
    converted['tick'] = int(hex[3] + hex[2],16)

    #Check what type packet we have
    converted['type'] = int(hex[4],16)

    #depending on type number we have different things

    #Converting a GPS packet
    if converted['type'] == 5:
        converted['GPSflags'] = int(hex[5],16)
        
        converted['altitude'] = int(hex[7] + hex[6],16)

        converted['latitude'] = float(struct.unpack('<i', packet[16:24].decode('hex'))[0])/10000000
        
        converted['longitude'] = float(struct.unpack('<i' , packet[24:32].decode('hex'))[0])/10000000
    
    if converted['type'] == 1:
        converted['state'] = int(hex[5],16)
        converted['accel'] = float(struct.unpack('<i' , packet[12:16].decode('hex')))
        converted['pres'] = float(struct.unpack('<h', packet[16:20].decode('hex'))) 
        converted['temp'] = float(struct.unpack('<h', packet[20:24].decode('hex')))
        converted['v_batt'] = float(struct.unpack('<h', packet[24:28].decode('hex')))
        converted['sense_d'] = float(struct.unpack('<h', packet[28:32].decode('hex')))
        converted['sense_m'] = float(struct.unpack('<h', packet[32:36].decode('hex')))
        
    return converted
