import gc

import esp
# import webrepl

import network
from ttgo_display import ttgo_display
import config

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
    display.tft.rotation(3)
    print('Connected!')
    for i, item in enumerate(sta_if.ifconfig()):
        display.text(item, i)


connect_to_wifi(config.SSID, config.wifi_passwd)
# webrepl.start(password=config.webrepl_passwd)



