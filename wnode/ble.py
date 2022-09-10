import time
import ubinascii
import bluetooth
import ustruct
import gc
# import 

from micropython import const


# Logging functions
import ulogger
import wnode.logging_handlers
logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical


# Data decode functions
def decode_adv_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2 : i + payload[i] + 1])
        i += 1 + payload[i]
    return result
def decode_adv_name(payload):
    n = decode_adv_field(payload, const(0x09))
    return str(n[0], "utf-8") if n else ""
def decode_raw_ruuvitag_data(addr, rssi, raw_data):
    # Remove meta data from adv_data
    raw_data = raw_data[10:]
    # Support only format 3 (RAWV1) and 5 (RAWV2)
    # Decode data and pass it back as dictionary
    if raw_data[4:6] == '03':
        data = _decode_raw_1(addr, rssi, ubinascii.unhexlify(raw_data))
    elif raw_data[4:6] == '05':
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
        'RSSI': rssi,
        'humidity': humidity,
        'temperature': temperature,
        'pressure': pressure,
        'acceleration_x': acceleration_x,
        'acceleration_y': acceleration_y,
        'acceleration_z': acceleration_z,
        'battery_voltage': battery_voltage,
        'last_update': time.time(),}
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
        'RSSI': rssi,
        'humidity': humidity,
        'temperature': temperature,
        'pressure': pressure,
        'acceleration_x': acceleration_x,
        'acceleration_y': acceleration_y,
        'acceleration_z': acceleration_z,
        'battery_voltage': battery_voltage,
        'tx_power': tx_power,
        'movement_counter': movement_counter,
        'measurement_sequence': measurement_sequence,
        'last_update': time.time(),}
    return data_dict

# Engine - The part of BLE module which is handling all tasks

class ble_engine():
    def __init__(self):
        self.ble = bluetooth.BLE()
        self.ble.irq(self._scan_irq)
        self.ble.active(True)
        self.allowed_devices = []
        self.blocked_devices = []
        self.scan_results = []
        self.beacons = []
        
        
        self._scanned_devices = []
        self._scan_ready = None
        self._reset_ble_device_irq_data_buffer()
    def _reset_ble_device_irq_data_buffer(self):
        self._addr = None
        self._rssi = None
        self._adv_data = None
    def _scan_irq(self, event, data):
        # BLE scan status definitions
        _IRQ_SCAN_RESULT = const(5)
        _IRQ_SCAN_DONE = const(6)
        if event == _IRQ_SCAN_RESULT:
            if self._addr == None:
                _, addr, _, rssi, adv_data = data
                self._addr = bytes(addr)
                self._rssi = rssi
                self._adv_data = bytes(adv_data)
        elif event == _IRQ_SCAN_DONE:
            self._scan_ready = True
    def scan(self, scan_time = 3):
        
        self._scan_ready = False
        self.scan_results = []
        self._scanned_devices = []
        
        info(f'Scanning Bluetooth devices for {scan_time} sec...')
        self.ble.gap_scan(scan_time * 1000, 400000, 40000, True)
        
        while self._scan_ready == False:
            if self._addr != None:
                address = ubinascii.hexlify(self._addr).decode("utf-8")
                if not address in self._scanned_devices:
                    if (len(self.allowed_devices) == 0 and not address in self.blocked_devices) or (address in self.allowed_devices):
                        debug(f'Advertisement from {address}')
                        self._scanned_devices.append(address)
                        name = decode_adv_name(self._adv_data) or "?"
                        data = ubinascii.hexlify(self._adv_data).decode("utf-8")
                        self.scan_results.append({'address':address, 'name':name, 'adv_data':data, 'RSSI':self._rssi})
                self._reset_ble_device_irq_data_buffer()
            else:
                time.sleep_ms(250)

        info('Scan done!')
    def active(self):
        self.ble.active(True)
    def deactive(self):
        self.ble.active(False)
    def search_beacons_from_scan_results(self):
        _RUUVITAG = "9904"

        self.beacons = []

        for device in self.scan_results:
            data = device['adv_data']
            if len(data) >= 14: #Check if beacon is RuuviTag
                if data[10:14] == _RUUVITAG:
                    address = device['address']
                    rssi = device['RSSI']
                    debug(f'RuuviTag found with address: {address}')
                    self.beacons.append(decode_raw_ruuvitag_data(address, rssi, data))

        return self.beacons


if __name__ is "__main__":
    eng = ble_engine()
    eng.scan(5)
    eng.search_beacons_from_scan_results()

