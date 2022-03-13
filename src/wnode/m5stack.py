
import machine
import time
import ulogger
import wnode.logging_handlers
import atom

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
if __name__ == '__main__':
    device = atom_matrix()
    device.red_signal()
    time.sleep(1)
    device.yellow_signal()
    time.sleep(1)
    device.green_signal()
    time.sleep(1)
    device.blue_signal()
