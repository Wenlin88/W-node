import gc
import time
import ubinascii
import machine
import esp
import webrepl

import network
import config
import homeassistant
from umqtt.robust import MQTTClient

from ruuvitag import RuuviTag
from ttgo_display import ttgo_display

gc.collect()
esp.osdebug(None)

def connect_to_wifi(ssid, pwd):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    display = ttgo_display.display()
    print('Connected!')
    for i, item in enumerate(sta_if.ifconfig()):
        display.text(item, i)


connect_to_wifi(config.SSID, config.wifi_passwd)
# webrepl.start(password=config.webrepl_passwd)
client_id = ubinascii.hexlify(machine.unique_id())
