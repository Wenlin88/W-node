# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import webrepl
import ttgo_display.ttgo_display as ttgo_display
from config import SSID, wifi_passwd, webrepl_passwd #IF you don't have config.py on your local directory, just make it and add these parameters with correct values there 
esp.osdebug(None)

def connect_to_wifi(ssid, pwd):
    import network
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
 
connect_to_wifi(SSID, wifi_passwd)

import webrepl
webrepl.start(password=webrepl_passwd)