
import network
import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import config
import re
import json

import ulogger
import wnode.logging_handlers
logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical


def merge_two_dicts(x,y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    # Python > 3.5 --> {**x, **y} - Python > 3.9 --> x | y
    return z

class ha_engine():
    def __init__(self, mqtt_client) -> None:
        self.mqtt_client = mqtt_client
        self.known_beacons = []
        self.supported_beacon_data_types = [
            'RuuviTagRAWv1',
            'RuuviTagRAWv2',
        ]
    def introduce_wnode_to_ha(self, friendly_name, device_type, hw_type, manufacturer, sw_version):
        info(f'Introduction on progress. Please wait...')
        relax_time_between_publish = 0.2
        name = friendly_name
        measurement_name = "Debug Message"
        
        friendly_name = name
        topic_base_name = re.sub('\W+','', friendly_name).lower()
        topic_name = re.sub('\W+','', measurement_name).lower()
        
        device_description = f"{device_type} - {hw_type}"
        manufacturer =  manufacturer
        sw_version = sw_version

        self._ha_device_id = topic_base_name
        self.wnode_debug_msg_topic = "homeassistant/sensor/" + topic_base_name + "/debug"
        
        msg = {
        "device": {
            "identifiers": [
            self._ha_device_id
            ],
            "manufacturer": manufacturer,
            "model": device_description,
            "name": friendly_name,
            "sw_version": sw_version
        },
        "icon": "mdi:message",
        "name": measurement_name,
        "state_class": "measurement",
        "state_topic": self.wnode_debug_msg_topic,
        "unique_id": topic_base_name +"_"+ topic_name
        }
        
        self.mqtt_client.connect()
        self.mqtt_client.publish(
            "homeassistant/sensor/" + topic_base_name + "/" + topic_name + "/config",
            msg=json.dumps(msg).encode(),
            qos = 1)

        time.sleep(relax_time_between_publish)
        self.mqtt_client.publish(
            "homeassistant/sensor/" +  topic_base_name + "/debug",
            msg='Default initialization done!'.encode(),
            qos = 1)

        measurement_name = "uptime"
        topic_name = re.sub('\W+','', measurement_name).lower()
        self.wnode_uptime_topic = "homeassistant/sensor/" + topic_base_name + "/uptime"

        msg = {
            "device": {
                "identifiers": [
                self._ha_device_id
                ],
            },
            "icon": "mdi:clock",
            "name": measurement_name,
            "state_class": "measurement",
            "state_topic": self.wnode_uptime_topic,
            "unique_id": topic_base_name +"_"+ topic_name
            }

        time.sleep(relax_time_between_publish)
        self.mqtt_client.publish(
            "homeassistant/sensor/" + topic_base_name + "/" + topic_name + "/config",
            msg=json.dumps(msg).encode(),
            qos = 1)

        time.sleep(relax_time_between_publish)
        self.mqtt_client.publish(
            "homeassistant/sensor/" +  topic_base_name + "/uptime",
            msg=str(time.ticks_ms()/1000).encode(),
            qos = 1)
        self.mqtt_client.disconnect()
        return True
    def introduce_new_measurement_to_exsitsting_sensor(self,measurement_name, friendly_name, unit = "V"):
        measurement_name = re.sub('\W+','', measurement_name).lower()
        device_name = re.sub('\W+','', friendly_name).lower()
        full_topic = "homeassistant/sensor/" + device_name + "/" + measurement_name
        msg = {
            "device": {
                "identifiers": [
                device_name
                ],
            },
            "name": measurement_name,
            "unit_of_measurement": unit,
            "state_class": "measurement",
            "state_topic": full_topic,
            "unique_id": device_name +"_"+ measurement_name
            }
        time.sleep(0.1)
        self.mqtt_client.connect()
        time.sleep(0.1)
        self.mqtt_client.publish(
            "homeassistant/sensor/" + device_name + "/" + measurement_name + "/config",
            msg=json.dumps(msg).encode(),
            qos = 1)
        self.mqtt_client.disconnect()
    def publish_measurement(self,measurement_name, friendly_name, value):
        measurement_name = re.sub('\W+','', measurement_name).lower()
        device_name = re.sub('\W+','', friendly_name).lower()
        time.sleep(0.1)
        self.mqtt_client.connect()
        time.sleep(0.1)
        self.mqtt_client.publish(
            "homeassistant/sensor/" +  device_name + "/" + measurement_name,
            msg=str(value).encode(),
            qos = 1)
        self.mqtt_client.disconnect()
    def publish_ble_beacon_data(self, beacon_data):
        for data in beacon_data:
            # If named tuple name is in knowns sensor types 
            if data['sensor_data_type'] in self.supported_beacon_data_types:
                # If sensor is known check if this specific sensor is already introduced to home assistant 
                if not data['mac'] in self.known_beacons:
                    debug(data['mac'] + " not known. Doing introduction...")
                    if data['sensor_data_type'] == 'RuuviTagRAWv1' or data['sensor_data_type'] == 'RuuviTagRAWv2':
                        info('Initializing new ruuvitag sensor...')
                        init_successful = self.introduce_ruuvitag_to_ha(data)
                        if not init_successful:
                            return False
                    debug(data['mac'] + " introduction done!")
                # Publish sensor data
                state_topic = 'homeassistant/sensor/' + data['mac'] + '/state'
                time.sleep(0.1)
                self.mqtt_client.connect()
                self.mqtt_client.publish(state_topic, msg=json.dumps(data).encode(), qos=0, retain=False)
                self.mqtt_client.disconnect()
            # Else it is not. Return false and print error that sensor is not in supported 
            else:
                warning('homeassistant mqtt sensor core is not supporting sensor type: ' + data['sensor_data_type'])
    def introduce_ruuvitag_to_ha(self, data):
        mqtt_client = self.mqtt_client
        mqtt_client.connect()

        relax_time_between_publish = 0.1
        device_info_part = {
            "device": {
                "identifiers": [
                "ruuvitag_"+data['mac']
                ],
                "manufacturer": "Ruuvi",
                "model": "RuuviTag",
                "name": data['mac'],
                "sw_version":  data['sensor_data_type']
                },}
        meas_part = {
            "device_class": "temperature",
            "name": data['mac'] + " Temperature",
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state",
            "unit_of_measurement": "°C", 
            "value_template": "{{ value_json.temperature}}",
            "unique_id": data['mac'] + "_temperature_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/temperature/config'
        time.sleep(relax_time_between_publish)
        mqtt_client.publish(
            config_topic,
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)).encode(),
            qos = 1)
        time.sleep(relax_time_between_publish)
        meas_part = {
            "device_class": "humidity",
            "name": data['mac'] + " Humidity", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "unit_of_measurement": "%", 
            "value_template": "{{ value_json.humidity}}",
            "unique_id": data['mac'] + "_humidity_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/humidity/config'
        mqtt_client.publish(
            config_topic,
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)).encode())
        time.sleep(relax_time_between_publish)
        meas_part = {
            "device_class": "voltage",
            "name": data['mac'] + " Battery Voltage", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "unit_of_measurement": "V", 
            "value_template": "{{ value_json.battery_voltage}}",
            "unique_id": data['mac'] + "_battery_voltage_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/battery_voltage/config'
        mqtt_client.publish(
            config_topic,
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)))
        time.sleep(relax_time_between_publish)
        meas_part = {
            "name": data['mac'] + " MAC", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{ value_json.mac}}",
            "unique_id": data['mac'] + "_mac_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/mac/config'
        mqtt_client.publish(
            config_topic, 
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)
        time.sleep(relax_time_between_publish)
        meas_part = {
            "device_class": "signal_strength",
            "name": data['mac'] + " RSSI",
            "unit_of_measurement": "dBm", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{ value_json.RSSI}}",
            "unique_id": data['mac'] + "_RSSI_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/RSSI/config'
        mqtt_client.publish(
            config_topic, 
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)
        time.sleep(relax_time_between_publish)
        meas_part = {
            "device_class": "pressure",
            "name": data['mac'] + " pressure",
            "unit_of_measurement": "hPa", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{ value_json.pressure}}",
            "unique_id": data['mac'] + "_pressure_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/pressure/config'
        mqtt_client.publish(
            config_topic, 
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)
        
        # Acceleration x introduction
        time.sleep(relax_time_between_publish)
        meas_part = {
            "name": data['mac'] + " acceleration x",
            "unit_of_measurement": "mg", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{value_json.acceleration_x}}",
            "unique_id": data['mac'] + "_acceleration_x_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/acceleration_x/config'
        mqtt_client.publish(
            config_topic, 
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)
        
        # Acceleration y introduction
        time.sleep(relax_time_between_publish)
        meas_part = {
            "name": data['mac'] + " acceleration y",
            "unit_of_measurement": "mg", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{value_json.acceleration_y}}",
            "unique_id": data['mac'] + "_acceleration_y_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/acceleration_y/config'
        mqtt_client.publish(
            config_topic, 
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)

        # Acceleration z introduction
        time.sleep(relax_time_between_publish)
        meas_part = {
            "name": data['mac'] + " acceleration z",
            "unit_of_measurement": "mg", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{value_json.acceleration_z}}",
            "unique_id": data['mac'] + "_acceleration_z_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/acceleration_z/config'
        mqtt_client.publish(
            config_topic, 
            msg=json.dumps(merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)

        time.sleep(relax_time_between_publish)
        self.known_beacons.append(data['mac'])
        mqtt_client.disconnect()
        return True

def debug_data_sets():
    beacon_data = [{'measurement_sequence': 55163, 'temperature': 20.08, 'last_update': 2949,
    'sensor_data_type': 'RuuviTagRAWv2', 'mac': 'e6b662d4e8c4', 'RSSI': -74, 'pressure': 993.95,
    'acceleration_x': -4, 'acceleration_y': -60, 'acceleration_z': 1012, 'battery_voltage': 2929,
    'tx_power': 4, 'humidity': 29.775, 'movement_counter': 215},
    {'humidity': 24.0, 'acceleration_x': 11, 'acceleration_y': 18, 'acceleration_z': 1060,
     'last_update': 2949, 'RSSI': -36, 'battery_voltage': 2941, 
    'sensor_data_type': 'RuuviTagRAWv1', 'mac': 'fa17408c975a', 'temperature': 28.43,
    'pressure': 994.39}]
    return beacon_data