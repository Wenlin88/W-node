import gc

import config
import esp
import webrepl

import network
import config
from ttgo_display import ttgo_display

gc.collect()
esp.osdebug(None)

# Initialize TTGO display -->
display = ttgo_display.display()
display.tft.rotation(2)

def connect_to_wifi(ssid, pwd):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass

    display.text(sta_if.ifconfig()[0], 0)
    print('Connected!')



connect_to_wifi(config.SSID, config.wifi_passwd)
webrepl.start(password=config.webrepl_passwd)

