import network
import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import config
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




class mqtt_engine():
    def __init__(self) -> None:
        pass
    def connect(self ,ssl = True):
        if ssl:
            f = open('client.key', "r")
            key_data = f.read()
            f.close()

            f = open('client.crt', "r")
            cert_data = f.read()
            f.close()

            client_id = ubinascii.hexlify(machine.unique_id())

            client = MQTTClient(
                client_id,
                server = config.ssl_mqtt_server,
                user = config.ssl_mqtt_user,
                password = config.ssl_mqtt_password,
                port = config.ssl_mqtt_port,
                ssl=True,
                ssl_params={'key':key_data, 'cert':cert_data})
        else:
            client_id = ubinascii.hexlify(machine.unique_id())
            client = MQTTClient(
                client_id,
                server = config.mqtt_server,
                user = config.mqtt_user,
                password = config.mqtt_password,
                port = config.mqtt_port,
                ssl=False,
                ssl_params={})


        self.client = client
        connection = self.check_mqtt_connection()
        if connection:
            return True
        else:
            return False
    # Check functions
    def check_mqtt_connection(self):
        try:
            self.client.connect()
            self.status = 'online'
            info('MQTT client status: online')
            self.client.disconnect()
            return True
        except:
            error('Connection to MQTT server failed!')
            self.status = 'offline'
            return False

if __name__ is "__main__":
    me = mqtt_engine()
    me.connect(ssl=False)