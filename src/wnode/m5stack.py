
import machine
import time
import ulogger
import wnode.logging_handlers
import atom
import math

logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical

class atom_matrix():
    signals_brightness = 3 
    def __init__(self):
        self.device = atom.Matrix()
    def status_signal(self, status):
        if status == 'error':
            self.red_signal()
        elif status == 'initializing':
            self.yellow_signal()
        elif status == 'online':
            self.green_signal()
        elif status == 'scanning':
            self.blue_signal()
        else:
            warning('Requested status signal not implemented on Atom matrix HW!')
    def red_signal(self):
        self.device.set_pixels_color(self.signals_brightness,0,0)
    def yellow_signal(self):
        self.device.set_pixels_color(self.signals_brightness,self.signals_brightness,0)
    def green_signal(self):
        self.device.set_pixels_color(0,self.signals_brightness,0)
    def blue_signal(self):
        self.device.set_pixels_color(0,0,self.signals_brightness)
    def init_adc(self, pin = 33):
        adc_pin = machine.Pin(pin)

        # Create an ADC object out of our pin object
        self.adc = machine.ADC(adc_pin)

        # 11 dB attenuation means full 0 - 3.3V range
        self.adc.atten(self.adc.ATTN_11DB)
        
    def read_adc(self, n_samples = 100):
        n_samples = n_samples
        val = 0
        for i in range(n_samples):
            val = val + self.adc.read()
            time.sleep(0.001)
        val = (val/n_samples) * (3.3 / 4095) + 0.1472037
        debug(val)
        return val
if __name__ == '__main__':
    atom = atom_matrix()
    atom.init_adc()

    u1 = atom.read_adc()
    r2 = 100e3
    vtot = 3.35
    r1 = u1*r2/(vtot-u1)
    print(r1)
    t = 1/(1/(25+273.15)-math.log(32762/r1)/4300)-273.15
    print(t)