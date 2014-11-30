from struct import unpack


def convert(packet):
    out = {}

    # Append serial number to list
    out['Serial'] = unpack('<H', packet[0:4].decode('hex'))[0]

    # Append Tick to list
    out['tick'] = unpack('<H', packet[4:8].decode('hex'))[0]

    # Check what type packet we have
    out['type'] = unpack('<B', packet[8:10].decode('hex'))[0]

    # Depending on type number we have different things

    # Converting a GPS packet
    if out['type'] == 5:
        out['GPSflags'] = unpack('<B', packet[10:12].decode('hex'))[0]

        out['altitude'] = unpack('<h', packet[12:16].decode('hex'))[0]

        out['latitude'] = float(unpack('<i', packet[16:24].decode('hex'))[0])/10000000

        out['longitude'] = float(unpack('<i', packet[24:32].decode('hex'))[0])/10000000

    # Converting a sensor packet
    if out['type'] == 10:
        pres_temp = unpack('<h', packet[16:20].decode('hex'))[0]
        temp_temp = unpack('<h', packet[20:24].decode('hex'))[0]
        v_batt_temp = unpack('<h', packet[24:28].decode('hex'))[0]

        out['state'] = unpack('<B', packet[10:12].decode('hex'))[0]
        out['accel'] = unpack('<h', packet[12:16].decode('hex'))[0]

        out['pres'] = -1*((pres_temp / 16.0) / 2047.0 + 0.095) / 0.009 * 1000.0
        out['temp'] = -1*((temp_temp - 19791.268) / 32728.0 * 1.25 / 0.00246 + 273.2)

        out['v_batt'] = v_batt_temp / 32767.0 * 5.0
        out['sense_d'] = unpack('<h', packet[28:32].decode('hex'))[0]

        out['sense_m'] = unpack('<h', packet[32:36].decode('hex'))[0]
        out['acceleration'] = float(unpack('<h', packet[36:40].decode('hex'))[0])/16

        out['speed'] = float(unpack('<h', packet[40:44].decode('hex'))[0])/16
        out['height'] = unpack('<h', packet[44:48].decode('hex'))[0]

        out['ground_accel'] = unpack('<h', packet[52:56].decode('hex'))[0]
        out['accel_plus_g'] = unpack('<h', packet[56:60].decode('hex'))[0]

        out['accel_minus_g'] = unpack('<h', packet[60:64].decode('hex'))[0]
    return out
