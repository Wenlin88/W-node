import ustruct
import ubinascii


def decode_raw_1(mac, rssi, data):
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
        '5': 5,
        'humidity': humidity,
        'temperature': temperature,
        'pressure': pressure,
        'acceleration_x': acceleration_x,
        'acceleration_y': acceleration_y,
        'acceleration_z': acceleration_z,
        'battery_voltage': battery_voltage,}
    return data_dict


def decode_raw_2(mac, rssi, data):
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
        '5': 5,
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
