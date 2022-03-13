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
    'hw_type': 'Atom matrix',
    'wifi': True,
    'mqtt': 1,
    'homeassistant': 1,
    'ble': 1
    }
wn = wnode.wnode_engine('W-Node', wnode_parameters)
wn.run_ble_beacon_scan_app()




