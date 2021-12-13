import time
import gc
from umqtt.simple import MQTTClient
import ubinascii
import machine
import config
from ttgo_display import ttgo_display


pin0 = machine.Pin(2, mode=machine.Pin.IN | machine.Pin.OUT, pull=machine.Pin.PULL_UP)
pwm0 = machine.PWM(pin0, freq=25000, duty=512)
display.text('Toimii!', 1)

while True:
    pwm0.duty(512+100)
    display.text('Out ---> In', 1)
    time.sleep(70)
    pwm0.duty(512-100)
    display.text('Out <--- In', 1)
    time.sleep(70)