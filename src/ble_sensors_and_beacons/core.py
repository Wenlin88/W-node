import struct
import ubinascii
import time
import ubluetooth as bluetooth


from micropython import const

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

# Known sensor and beacon company identifiers
_RUUVITAG = "9904"

def debug(msg):
    # print(msg)
    pass
def info(msg):
    print(msg)

# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)

def decode_adv_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2 : i + payload[i] + 1])
        i += 1 + payload[i]
    return result
def decode_adv_name(payload):
    n = decode_adv_field(payload, _ADV_TYPE_NAME)
    return str(n[0], "utf-8") if n else ""


class scanner:
    scan_time = 10 # secs
    scan_active = False
    raw_data_list = []
    device_addreses = []
    device_data = []

    def scan(self):
        info('Starting BLE beacon scan...')
        # Initialize Bluetooth
        ble = bluetooth.BLE()
        ble.active(True)
        ble.irq(self._irq_handler)
        self.device_addreses = []

        # Scan process
        self.scan_active = True
        ble.gap_scan(self.scan_time * 1000, 400000, 200000, True)
        while self.scan_active is True:
            time.sleep(0.2)
        info('Scan done!')
        ble.active(False)
    def publish_beacon_data(self, publish_callback):
        pass
    def get_adverticed_addresses(self):
        '''Get all advertised addresses during scan'''   
    def _irq_handler(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, connectable, rssi, adv_data = data
            addr = ubinascii.hexlify(addr).decode("utf-8")
            name = decode_adv_name(adv_data) or "?"
            data = ubinascii.hexlify(adv_data).decode("utf-8")
            debug('Advertisement from: {} with name {:<15} and data: {}' .format(addr, name, data))
            self._detect_known_sensors_and_beacons(addr, data, name, rssi)

        elif event == _IRQ_SCAN_DONE:
            self.scan_active = False
    def _detect_known_sensors_and_beacons(self, addr, data, name, rssi):
        if not addr in [item['address'] for item in self.device_data]:
            if name == "MJ_HT_V1":
                info('MJ_HT_V1 found with address: {}'.format(addr))
                self.device_data.append({'address':addr, 'name':name, 'data':data, 'rssi':rssi})
            elif len(data) >= 14: #Check if beacon is RuuviTag
                if data[10:14] == _RUUVITAG:
                    info('RuuviTag found with address: {}'.format(addr))
                    self.device_data.append({'address':addr, 'name':name, 'data':data, 'rssi':rssi})
          



