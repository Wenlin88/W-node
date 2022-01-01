import time
import gc
import ubinascii
import machine
from umqtt.simple import MQTTClient
import homeassistant.mqtt_sensor
from ttgo_display import ttgo_display
from micropython import const
import ble_sensors_and_beacons
import config

print('Memory at beginning')
print('Allocated: ' + str(gc.mem_alloc()))
print('Free: ' + str(gc.mem_free()))


mqtt_sensor_handler = homeassistant.mqtt_sensor.mqtt_sensors_handler()
display = ttgo_display.display()
display.tft.rotation(3)
display.text('Running main!', 0)

client_id = ubinascii.hexlify(machine.unique_id())

f = open('client.key', "r")
key_data = f.read()
f.close()

f = open('client.crt', "r")
cert_data = f.read()
f.close()

i = 0

bsb = ble_sensors_and_beacons.scanner()

client = MQTTClient(
    client_id,
    server = config.mqtt_server,
    user = config.mqtt_user,
    password = config.mqtt_password,
    port = 8883,
    keepalive = 1000,
    ssl=True,
    ssl_params={'key':key_data,'cert':cert_data})

while True:
    # try:
    bsb.scan()
    gc.collect()
    print('Connect to MQTT broker!')
    client.connect(clean_session=True)
    i += 1
    client.publish('W-node/debug', msg=str(i).encode(), qos=0, retain=False)
    client.disconnect()
    display.text('Loops: ' + str(i), 1)

    break

