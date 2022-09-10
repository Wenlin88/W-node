import gc
import time
from machine import Pin
import ubinascii
import machine
import micropython
import config
from umqtt.simple import MQTTException
import neopixel
from micropython import const
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
    'hw_type': '',
    'wifi': 0,
    'mqtt': 0,
    'homeassistant': 0,
    'ble': 1,
    }

retry_count = 0
while True:
    try:
        wn = wnode.wnode_engine('W-Node', wnode_parameters)
        while True:
            wn.ble.scan(10)
            beacon_data = wn.ble.search_beacons_from_scan_results()
            print(beacon_data)
            info('Sleeping for 5 sec....')
            time.sleep(5)
            print('Toimii')
    except OSError as e:
        if retry_count < 5:
            warning('OSError. Retrying...')
            retry_count += 1
        else:
            error('Two many OSErrors! Restarting..')
            machine.reset()
    except MQTTException as e:
        if retry_count < 5:
            warning('MQTTException. Retrying...')
            retry_count += 1
        else:
            error('Two many MQTTException! Restarting..')
            machine.reset()
    except KeyboardInterrupt as e: 
        print('Stopping main...')
        break    
    except Exception as e:
        if retry_count < 5:
            warning(f'Undefined error: {e}. Retrying...')
            retry_count += 1
        else:
            error(f'Two many Undefined errors: {e}! Restarting...')
            machine.reset()

