import time
import gc
from umqtt.simple import MQTTClient
import ubinascii
import machine
import config
import homeassistant.mqtt_sensor
import ruuvitag
from ttgo_display import ttgo_display



mqtt_sensor_handler = homeassistant.mqtt_sensor.Core(client)
display = ttgo_display.display()
display.text('Running main!', 0)
display.text('Successful runs: ', 1)

i = 1
while True:
    try:
        gc.collect()
        client_id = ubinascii.hexlify(machine.unique_id())
        client = MQTTClient(
            client_id,
            server = config.mqtt_server,
            user = config.mqtt_user,
            password = config.mqtt_password,
            port = 8883,
            ssl=True,
            ssl_params={})
        time.sleep(1)
        ruuvi = ruuvitag.RuuviTag(callback_handler = mqtt_sensor_handler.append_sensor_data)
        client.disconnect()
        ruuvi.scan()
        time.sleep(30)
        i += 1
        display.text(str(i), 2)
        break

        
    except Exception as e:
        print(e)
        display.text('Main FAIL!', 3)
        break

