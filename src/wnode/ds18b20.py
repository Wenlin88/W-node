import time
import ubinascii
import machine
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




class engine():
    def __init__(self, mqtt_client = None, display = None, friendly_name = "W-node dev") -> None:
        if display != None:
            if hasattr(display, 'hw_type'):
                self.hw_type = display.hw_type
        self.mqtt_client = mqtt_client
        self.display = display
        self.ds_sensor = None
        self.ds_sensor_id = None
        self.friendly_name = friendly_name
    # Read functions
    def read_DS18B20_measurement(self):
        if not self.ds_sensor == None:
            self.ds_sensor.convert_temp()
            T1 = self.ds_sensor.read_temp(self.ds_sensor_id)
            info(f'DS18B20 temperature: {round(T1,2)}C\u00B0')
            if self.hw_type == 'TTGO display':
                self.display.text('T1:',2)
                self.display.text(str(round(T1,2)),3)
            if self.mqtt_client != None:
                self._publish_DS18B20_meas(T1)
        else:
            error('DS18B20 not initialized!')
    # Initialization functions
    def init_DS18B20_measurement(self, pin):
        import onewire, ds18x20
        ds_pin = machine.Pin(pin)
        ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        sensors = ds_sensor.scan()
        number_of_sensors = len(sensors)
        info(f'Found {number_of_sensors} DS device(s)!')

        if number_of_sensors == 1:
            sensor = sensors[0]
            ds_sensor.convert_temp()
            T1 = ds_sensor.read_temp(sensor)
            info(f'DS18B20 temperature: {round(T1,2)}C\u00B0')
            if self.hw_type == 'TTGO display':
                self.display.text('T1:',2)
                self.display.text(str(round(T1,2)),3)
            if self.mqtt_client != None:
                self._init_ha_for_DS18B20_meas()
            self.ds_sensor = ds_sensor
            self.ds_sensor_id = sensor
        else:
            info('W-Node is not yet supporting multiple DS18B20 sensors!')
    def _init_ha_for_DS18B20_meas(self):    
        name = self.friendly_name
        measurement_name = "Temperature"
        
        friendly_name = name
        topic_base_name = re.sub('\W+','', friendly_name).lower()
        topic_name = re.sub('\W+','', measurement_name).lower()
        
        self._device_id = topic_base_name
        self._DS18B20_topic = "homeassistant/sensor/" + topic_base_name + "/temperature"

        msg = {
            "device": {
                "identifiers": [
                self._device_id
                ],
            },
            "device_class": "temperature",
            "name": measurement_name,
            "unit_of_measurement": "\u00b0C",
            "state_class": "measurement",
            "state_topic": self._DS18B20_topic,
            "unique_id": topic_base_name +"_"+ topic_name
            }

        self.mqtt_client.connect()
        time.sleep(0.1)
        self.mqtt_client.publish(
            "homeassistant/sensor/" + topic_base_name + "/" + topic_name + "/config",
            msg=json.dumps(msg).encode('UTF-16'),
            qos = 1)
        time.sleep(0.1)
        self.mqtt_client.disconnect()
    def _publish_DS18B20_meas(self,T):
        self.mqtt_client.connect()
        time.sleep(0.1)
        self.mqtt_client.publish(
            self._DS18B20_topic,
            msg=str(round(T,2)).encode(),
            qos = 0)
        time.sleep(0.1)
        self.mqtt_client.disconnect()

if __name__ == '__main__':
    import wnode.ttgo as ttgo
    import wnode.mqtt as mqtt
    import wnode.ha as ha
    mqtt = mqtt.mqtt_engine()
    connection = mqtt.connect(ssl = False)
    ha = ha.ha_engine(mqtt.client)
    friendly_name = 'W-node dev'
    status = ha.introduce_wnode_to_ha(friendly_name, 'Temperature reader', 'TTGO', 'Henri Wenlin', '0.0.0')
    display = ttgo.display_engine()
    ds = engine(display = display, friendly_name = friendly_name, mqtt_client = mqtt.client)
    ds.init_DS18B20_measurement(25)
    for i in range(10):
        time.sleep(1)
        ds.read_DS18B20_measurement()