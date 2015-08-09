from struct import unpack

def byte_unpacker(conversion_type, data):
    return unpack(conversion_type, data.decode('hex'))[0]

def convert_gps_packet(packet):
    out = dict()

    out['GPSflags'] = byte_unpacker('<B', packet[12:14])
    out['GPSaltitude'] = byte_unpacker('<h', packet[14:18])
    out['latitude'] = byte_unpacker('<i', packet[18:26])/10000000.0
    out['longitude'] = byte_unpacker('<i', packet[26:34])/10000000.0

    return out


def convert_sensor_packet(packet):
    out = dict()

    out['temperature'] = byte_unpacker('<h', packet[26:30]) / 100.0
    out['battery_voltage'] = byte_unpacker('<h', packet[42:46])
    out['pressure'] = byte_unpacker('<i', packet[18:26]) / 10.0

    out['state'] = byte_unpacker('<B', packet[12:14])
    out['accelerometer'] = byte_unpacker('<h', packet[14:18])
    out['drogue_continuity'] = byte_unpacker('<h', packet[46:50])

    out['main_continuity'] = byte_unpacker('<h', packet[50:54])
    out['acceleration'] = byte_unpacker('<h', packet[30:34])/16.0
    out['speed'] = byte_unpacker('<h', packet[34:38])/16.0

    out['height'] = byte_unpacker('<h', packet[38:42])

    return out


def convert_config_packet(packet):
    out = dict()

    out['device_type'] = byte_unpacker('<B', packet[12:14])
    out['flight_number'] = byte_unpacker('<H', packet[14:18])
    out['config_major'] = byte_unpacker('<B', packet[18:20])

    out['config_minor'] = byte_unpacker('<B', packet[20:22])
    out['apogee_delay'] = byte_unpacker('<H', packet[22:26])
    out['main_deploy'] = byte_unpacker('<H', packet[26:30])

    out['max_log_size'] = byte_unpacker('<H', packet[30:34])

    out['callsign'] = ''
    for i in range(34, 50, 2):
        out['callsign'] += byte_unpacker('<c', packet[i:i+2])

    out['software_version'] = ''
    for i in range(50, 66, 2):
        out['software_version'] += byte_unpacker('<c', packet[i:i+2])

    return out


def convert_calibration_packet(packet):
    out = dict()
    out['ground_pressure'] = byte_unpacker('<i', packet[20:28])
    out['ground_acceleration'] = byte_unpacker('<h', packet[28:32])
    out['acceleration_+_gravity'] = byte_unpacker('<h', packet[32:36])
    out['acceleration_-_gravity'] = byte_unpacker('<h', packet[36:40])

    return out


def pass_function(packet):
    return {}


def convert_satellite_packet(packet):
    out = dict()

    out['num_channels'] = byte_unpacker('<B', packet[12:14])

    satellites = []
    for i in range(14, 48, 4):
        # FIX needs to be tested
        # Stored as a SVID and sigQual tuple
        SVID = byte_unpacker('<B', packet[i:i+2])
        signal_quality = byte_unpacker('<B', packet[i+2:i+4])
        satellites.append((SVID, signal_quality))

    out['satellites'] = satellites

    return out


def verify_packet(packet):
    # testing checsum

    running_sum = 0
    for i in range(2, 70, 2):
        running_sum += byte_unpacker('<B', packet[i:i+2])

    if byte_unpacker('<B', packet[70:72]) == (90 + running_sum) % 256:
        return True
    else:
        return False



def convert(packet):
    out = dict()

    options = {4: convert_config_packet,
               5: convert_gps_packet,
               6: convert_satellite_packet,
               10: convert_sensor_packet,
               11: convert_calibration_packet,
               27: pass_function,
               168: pass_function
                }

    out['length'] = packet[0:2]
    # Append serial number to list
    out['serial'] = byte_unpacker('<H', packet[2:6])

    # Append Tick to list
    out['tick'] = byte_unpacker('<H', packet[6:10])

    # Check what type packet we have
    out['type'] = byte_unpacker('<B', packet[10:12])
    # Depending on type number we have different things

    out.update(options[out['type']](packet))
    return out
