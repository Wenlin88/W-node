# from collections import namedtuple
import json
import time

def info(msg):
    print(msg)
def debug(msg):
    print(msg)
def warning(msg):
    print(msg)


class Core():
    known_sensors = []
    def __init__(self, mqtt_client) -> None:
        self.mqtt_client = mqtt_client
        self.knonw_sensor_IDs = []
        self.publish_buffer = []
        self.supported_sensor_data_types = [
            'RuuviTagRAWv1',
            'RuuviTagRAWv2',
        ]
    def _merge_two_dicts(self,x,y):
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        # Python > 3.5 --> {**x, **y} - Python > 3.9 --> x | y
        return z
    def publish(self,data):
        # If named tuple name is in knowns sensor types 
        if data['sensor_data_type'] in self.supported_sensor_data_types:
            # If sensor is known check if this specific sensor is already introduced to home assistant 
            if not data['mac'] in self.knonw_sensor_IDs:
                debug(data['mac'] + " not known. Doing introduction...")
                if data['sensor_data_type'] == 'RuuviTagRAWv1' or data['sensor_data_type'] == 'RuuviTagRAWv2':
                    info('Initializing new ruuvitag sensor...')
                    init_successful = self._init_ruuvitag_sensor(data)
                    if not init_successful:
                        return False
                debug(data['mac'] + " introduction done!")
            # Publish sensor data
            state_topic = 'homeassistant/sensor/' + data['mac'] + '/state'
            debug(state_topic + ' - ' + json.dumps(data))
            self.mqtt_client.publish(state_topic, msg=json.dumps(data).encode(), qos=0, retain=False)
        # Else it is not. Return false and print error that sensor is not in supported 
        else:
            warning('homeassistant mqtt sensor core is not supporting sensor type: ' + data['sensor_data_type'])
            return False
        return True
    def append_sensor_data(self,data):
        self.publish_buffer.append(data)
    def print_data_on_buffer(self):
        debug('Printing data on publish buffer...')
        for data in self.publish_buffer:
            print(data)
        debug('Print done!')
    def _init_ruuvitag_sensor(self, data):
        relax_time_between_publish = 0.01
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
        self.mqtt_client.publish(
            config_topic,
            msg=json.dumps(self._merge_two_dicts(device_info_part,meas_part)).encode(),
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
        self.mqtt_client.publish(
            config_topic,
            msg=json.dumps(self._merge_two_dicts(device_info_part,meas_part)).encode())
        time.sleep(relax_time_between_publish)
        meas_part = {
            "device_class": "voltage",
            "name": data['mac'] + " Battery Voltage", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "unit_of_measurement": "V", 
            "value_template": "{{ value_json.battery_voltage}}",
            "unique_id": data['mac'] + "_battery_voltage_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/battery_voltage/config'
        self.mqtt_client.publish(
            config_topic,
            msg=json.dumps(self._merge_two_dicts(device_info_part,meas_part)))
        time.sleep(relax_time_between_publish)
        meas_part = {
            "name": data['mac'] + " MAC", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{ value_json.mac}}",
            "unique_id": data['mac'] + "_mac_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/mac/config'
        self.mqtt_client.publish(
            config_topic, 
            msg=json.dumps(self._merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)
        time.sleep(relax_time_between_publish)
        meas_part = {
            "device_class": "signal_strength",
            "name": data['mac'] + " rssi",
            "unit_of_measurement": "dBm", 
            "state_topic": "homeassistant/sensor/" + data['mac'] +  "/state", 
            "value_template": "{{ value_json.rssi}}",
            "unique_id": data['mac'] + "_rssi_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data['mac'] + '/rssi/config'
        self.mqtt_client.publish(
            config_topic, 
            msg=json.dumps(self._merge_two_dicts(device_info_part,meas_part)), 
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
        self.mqtt_client.publish(
            config_topic, 
            msg=json.dumps(self._merge_two_dicts(device_info_part,meas_part)), 
            qos=0, 
            retain=False)
        
        self.knonw_sensor_IDs.append(data['mac'])

        return True
