import time
import ubinascii
import machine
from umqtt.simple2 import MQTTClient
import re
import json

def debug(msg):
    print(msg)
def info(msg):
    print(msg)
def warning(msg):
    print(msg)
def error(msg):
    print(msg)


class ds18b20_engine():
    def __init__(self) -> None:
        self.self.ds_sensor = None
        self.ds_sensor_id = None
        # Read functions
    def read_DS18B20_measurement(self):
        if not self.ds_sensor == None:
            self.ds_sensor.convert_temp()
            T1 = self.ds_sensor.read_temp(self.ds_sensor_id)
            info(f'DS18B20 temperature: {round(T1,2)}C\u00B0')
            if self.hw_type == 'TTGO display':
                self.display.text('T1:',2)
                self.display.text(str(round(T1,2)),3)
            if self.ha_status == 'online':
                self._publish_DS18B20_meas(T1)
        else:
            error('DS18B20 not initialized!')
    # Initialization functions
    def init_DS18B20_measurement(self, pin):
        import onewire, ds18x20
        ds_pin = machine.Pin(pin)
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        sensors = ds_sensor.scan()
        info(f'Found {len(sensors)} DS device(s)!')

        if len(sensors) == 1:
            sensor = sensors[0]
            ds_sensor.convert_temp()
            T1 = ds_sensor.read_temp(sensor)
            info(f'DS18B20 temperature: {round(T1,2)}C\u00B0')
            if self.hw_type == 'TTGO display':
                self.display.text('T1:',2)
                self.display.text(str(round(T1,2)),3)
            if self.ha_status == 'online':
                self._init_ha_for_DS18B20_meas()
        
            self.ds_sensor = ds_sensor
            self.ds_sensor_id = sensor
        else:
            info('W-Node is not yet supporting multiple DS18B20 sensors!')
    def _init_ha_for_DS18B20_meas(self):
        
        name = self.friendly_name
        measurement_name = "Temperature"
        
        client_id = ubinascii.hexlify(machine.unique_id())
        friendly_name = name
        topic_base_name = re.sub('\W+','', friendly_name).lower()
        topic_name = re.sub('\W+','', measurement_name).lower()
        self._ha_DS18B20_topic = "homeassistant/sensor/" + topic_base_name + "/temperature"

        msg = {
            "device": {
                "identifiers": [
                self._ha_device_id
                ],
            },
            "device_class": "temperature",
            "name": measurement_name,
            "unit_of_measurement": "\u00b0C",
            "state_class": "measurement",
            "state_topic": self._ha_DS18B20_topic,
            "unique_id": topic_base_name +"_"+ topic_name + "_" + client_id.decode()
            }

        self.mqtt_client.connect()
        self.mqtt_client.publish(
            "homeassistant/sensor/" + topic_base_name + "/" + topic_name + "/config",
            msg=json.dumps(msg).encode('UTF-16'),
            qos = 1)
        self.mqtt_client.disconnect()
    def _publish_DS18B20_meas(self,T):
        self.mqtt_client.connect()
        self.mqtt_client.publish(
            self._ha_DS18B20_topic,
            msg=str(round(T,2)).encode(),
            qos = 0)
        time.sleep(0.3)
        self.mqtt_client.publish(
            self._ha_uptime_topic,
            msg=str(time.ticks_ms()/1000).encode(),
            qos = 0)
        
        self.mqtt_client.disconnect()