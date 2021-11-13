# import esp
# import webrepl
# import ttgo_display.ttgo_display as ttgo_display
# import time
# from umqtt.simple import MQTTClient
# import ubinascii
# import machine
# import micropython
# import network
# import gc
# gc.collect()

# client_id = ubinascii.hexlify(machine.unique_id())

# def restart_and_reconnect():
#   print('Failed to connect to MQTT broker. Reconnecting...')
#   time.sleep(10)
#   machine.reset()

# try:
#   client = connect_and_subscribe()
# except OSError as e:
#   restart_and_reconnect()

# while True:
#   try:
#     new_message = client.check_msg()
#     if new_message != 'None':
#       client.publish(topic_pub, b'received')
#     time.sleep(1)
#   except OSError as e:
#     restart_and_reconnect()


with open('client.key') as f:
    key_data = f.read()

with open('client.crt') as f:
    cert_data = f.read()

client = MQTTClient(
    'W-node', 
    server = config.mqtt_server,
    user = 'xxxxxxx',
    password = 'xxxxxxx',
    port = 8883, 
    ssl=True,
    ssl_params={"key":key_data,"cert":cert_data})

client.connect()

client.publish(
    topic = 'testi/testi', 
    msg = 'Nyt tulee läpi niin et vaaditaan certi', 
    retain=False, qos=0,)

