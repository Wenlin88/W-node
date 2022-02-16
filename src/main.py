import gc
import time
import ubinascii
import machine
import micropython
import config

import network
import config
import urequests
import re
import wnode
import ulogger

def memory_usage_check(msg) -> None:
    print(msg)
    print('Allocated: ' + str(gc.mem_alloc()))
    print('Free: ' + str(gc.mem_free()))
def get_key_and_cert_data():
    f = open('client.key', "r")
    key_data = f.read()
    f.close()

    f = open('client.crt', "r")
    cert_data = f.read()
    f.close()

    return key_data, cert_data

import ulogger
import wnode.logging_handlers

logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical

memory_usage_check(msg = 'Memory at beginning')

wnode_parameters = {
    'hw_type': 'ATOM',
    'wifi': True,
    'mqtt': True,
    'homeassistant': True,
    'ble': True
    }
wn = wnode.wnode_engine('W-Node 2', wnode_parameters)

retry_count = 0
while True:
    try:
        gc.collect()
        time.sleep(0.1)
        wn.scan_ble_beacons(5)
        time.sleep(0.1)
        wn.status_update()
        time.sleep(1)

    except KeyboardInterrupt as e: 
        print('Stopping main...')
        break


