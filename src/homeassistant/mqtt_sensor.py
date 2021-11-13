from collections import namedtuple
import json

class Core():
    known_sensors = []
    def __init__(self, mqtt_client) -> None:
        
        self.mqtt_client = mqtt_client
        self.knonw_sensor_IDs = []

        self.supported_sensor_types = [
            'RuuviTagRAWv1',
        ]
    def post(self, data):
        # If named tuple name is in knowns sensor types 
        if type(data).__name__ in self.supported_sensor_types:
            # If sensor is known check if this specific sensor is already introduced to home assistant 
            if not data.mac in self.knonw_sensor_IDs:
                print(data.mac + " not known. Doing introduction...")
                if type(data).__name__ == 'RuuviTagRAWv1':
                    init_successful = self.init_RuuviTagRAWv1_sensor(data)
                    if not init_successful:
                        return False
                print(data.mac + " introduction done!")
            # Publish sensor data
            state_topic = 'homeassistant/sensor/' + data.mac + '/state'
            self.mqtt_client.publish(state_topic, payload=json.dumps(data._asdict()), qos=0, retain=False)
            return True
        # Else it is not. Return false and print error that sensor is not in supported 
        else:
            print('homeassistant mqtt sensor core is not supporting sensor type: ' + type(data).__name__)
    def init_RuuviTagRAWv1_sensor(self, data):

        device_info_part = {
            "device": {
                "identifiers": [
                "ruuvitag_"+data.mac
                ],
                "manufacturer": "Ruuvi",
                "model": "RuuviTag",
                "name": data.mac,
                "sw_version":  type(data).__name__
                },}
        meas_part = {
            "device_class": "temperature",
            "name": data.mac + " Temperature", 
            "state_topic": "homeassistant/sensor/" + data.mac +  "/state", 
            "unit_of_measurement": "°C", 
            "value_template": "{{ value_json.temperature}}",
            "unique_id": data.mac + "_temperature_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data.mac + '/temperature/config'
        self.mqtt_client.publish(
            config_topic, 
            payload=json.dumps({**device_info_part, **meas_part}), 
            qos=0, 
            retain=False)

        meas_part = {
            "device_class": "humidity",
            "name": data.mac + " Humidity", 
            "state_topic": "homeassistant/sensor/" + data.mac +  "/state", 
            "unit_of_measurement": "%", 
            "value_template": "{{ value_json.humidity}}",
            "unique_id": data.mac + "_humidity_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data.mac + '/humidity/config'
        self.mqtt_client.publish(
            config_topic, 
            payload=json.dumps({**device_info_part, **meas_part}), 
            qos=0, 
            retain=False)
        
        meas_part = {
            "device_class": "voltage",
            "name": data.mac + " Battery Voltage", 
            "state_topic": "homeassistant/sensor/" + data.mac +  "/state", 
            "unit_of_measurement": "V", 
            "value_template": "{{ value_json.battery_voltage}}",
            "unique_id": data.mac + "_battery_voltage_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data.mac + '/battery_voltage/config'
        self.mqtt_client.publish(
            config_topic, 
            payload=json.dumps({**device_info_part, **meas_part}), 
            qos=0, 
            retain=False)
        
        meas_part = {
            "name": data.mac + " MAC", 
            "state_topic": "homeassistant/sensor/" + data.mac +  "/state", 
            "value_template": "{{ value_json.mac}}",
            "unique_id": data.mac + "_mac_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data.mac + '/mac/config'
        self.mqtt_client.publish(
            config_topic, 
            payload=json.dumps({**device_info_part, **meas_part}), 
            qos=0, 
            retain=False)
        
        meas_part = {
            "device_class": "signal_strength",
            "name": data.mac + " rssi",
            "unit_of_measurement": "dBm", 
            "state_topic": "homeassistant/sensor/" + data.mac +  "/state", 
            "value_template": "{{ value_json.rssi}}",
            "unique_id": data.mac + "_rssi_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data.mac + '/rssi/config'
        self.mqtt_client.publish(
            config_topic, 
            payload=json.dumps({**device_info_part, **meas_part}), 
            qos=0, 
            retain=False)
        
        meas_part = {
            "device_class": "pressure",
            "name": data.mac + " pressure",
            "unit_of_measurement": "hPa", 
            "state_topic": "homeassistant/sensor/" + data.mac +  "/state", 
            "value_template": "{{ value_json.pressure}}",
            "unique_id": data.mac + "_pressure_ruuvitag",}
        config_topic = 'homeassistant/sensor/' + data.mac + '/pressure/config'
        self.mqtt_client.publish(
            config_topic, 
            payload=json.dumps({**device_info_part, **meas_part}), 
            qos=0, 
            retain=False)
        
        self.knonw_sensor_IDs.append(data.mac)

        return True
