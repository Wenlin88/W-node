import ustruct
import ubinascii
import ulogger
import wnode.logging_handlers

logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical

def decode_raw_ruuvitag_data(addr, rssi, raw_data):
    # Remove meta data from adv_data
    raw_data = raw_data[10:]
    # Support only format 3 (RAWv1) and 5 (RAWv2)
    # Decode data and pass it back as dict
    if raw_data[4:6] == b'03':
        data = _decode_raw_1(addr, rssi, ubinascii.unhexlify(raw_data))
    elif raw_data[4:6] == b'05':
        data = _decode_raw_2(addr, rssi, ubinascii.unhexlify(raw_data))
    else:
        data = None
    return data
def _decode_raw_1(mac, rssi, data):
    """RuuviTag RAW 1 decoder"""
    humidity = data[3] / 2

    temperature = data[4] + data[5] / 100
    if temperature > 128:
        temperature -= 128
        temperature = round(0 - temperature, 2)

    pressure = list(ustruct.unpack("!H", data[6:8]))[0] + 50000
    pressure = pressure/100

    acceleration_x = list(ustruct.unpack("!h", data[8:10]))[0]
    acceleration_y = list(ustruct.unpack("!h", data[10:12]))[0]
    acceleration_z = list(ustruct.unpack("!h", data[12:14]))[0]

    battery_voltage = list(ustruct.unpack("!H", data[14:16]))[0]

    data_dict = {
        'sensor_data_type': 'RuuviTagRAWv1',
        'mac': mac,
        'rssi': rssi,
        'humidity': humidity,
        'temperature': temperature,
        'pressure': pressure,
        'acceleration_x': acceleration_x,
        'acceleration_y': acceleration_y,
        'acceleration_z': acceleration_z,
        'battery_voltage': battery_voltage,}
    return data_dict
def _decode_raw_2(mac, rssi, data):
    """RuuviTag RAW 2 decoder"""
    temperature = list(ustruct.unpack("!h", data[3:5]))[0] * 0.005

    humidity = list(ustruct.unpack("!H", data[5:7]))[0] * 0.0025

    pressure = list(ustruct.unpack("!H", data[7:9]))[0] + 50000
    pressure = pressure/100


    acceleration_x = list(ustruct.unpack("!h", data[9:11]))[0]
    acceleration_y = list(ustruct.unpack("!h", data[11:13]))[0]
    acceleration_z = list(ustruct.unpack("!h", data[13:15]))[0]

    power_bin = bin(list(ustruct.unpack("!H", data[15:17]))[0])[2:]
    battery_voltage = int(power_bin[:11], 2) + 1600
    tx_power = int(power_bin[11:], 2) * 2 - 40

    movement_counter = data[18]

    measurement_sequence = list(ustruct.unpack("!H", data[18:20]))[0]

    data_dict = {
        'sensor_data_type': 'RuuviTagRAWv2',
        'mac': mac,
        'rssi': rssi,
        'humidity': humidity,
        'temperature': temperature,
        'pressure': pressure,
        'acceleration_x': acceleration_x,
        'acceleration_y': acceleration_y,
        'acceleration_z': acceleration_z,
        'battery_voltage': battery_voltage,
        'tx_power': tx_power,
        'movement_counter': movement_counter,
        'measurement_sequence': measurement_sequence,}
    return data_dict

# if __name__ is "__main__":
#     print(decode_raw_ruuvitag_data('e6b662d4e8c4', '-93', b'0201061bff9904050d7e2922c07500ecfd6cfd0ca33677bb80e6b662d4e8c4'))
#     print(decode_raw_ruuvitag_data('fa17408c975a', '-54', b'02010611ff990403391715c0a100120021041e0b83'))