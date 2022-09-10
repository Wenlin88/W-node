
import machine
import ulogger
import wnode.logging_handlers


logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical


class display_engine():
    def __init__(self):
        import st7789
        self.hw_type  = 'TTGO display'        
        spi = machine.SPI(2, baudrate=20000000,
            polarity=1,
            phase=0,
            sck=machine.Pin(18),
            mosi=machine.Pin(19),
            miso=machine.Pin(13))
        display = st7789.ST7789(spi,
            135,
            240,
            reset=machine.Pin(23, machine.Pin.OUT),
            cs=machine.Pin(5, machine.Pin.OUT),
            dc=machine.Pin(16, machine.Pin.OUT),
            backlight=machine.Pin(4, machine.Pin.OUT),
            rotation=0)
        display.rotation(1)
        display.fill(0)
        display.init()
        self.tft = display
    def text(self, msg, row):
        import st7789
        import wnode.fonts.vga2_16x32 as font
        self.tft.text(
            font,
            msg,
            0,
            (font.HEIGHT + 2) * row,
            st7789.color565(255, 255, 255),
            st7789.color565(0,0,0)
            )

class tcell():
    "https://github.com/LilyGO/TTGO-T-Cell"
    def blink_led(self):
        import time
        from machine import Pin
        led=Pin(21,Pin.OUT)        #create LED object from pin2,Set Pin2 to output
        led.value(1)            #Set led turn on
        time.sleep(0.5)
        led.value(0)            #Set led turn off
        time.sleep(0.5)
        led.value(1)   
        time.sleep(0.5)
        led.value(0)   
    def read_battery_voltage(self):
        adc_pin = machine.Pin(35)

        # Create an ADC object out of our pin object
        adc = machine.ADC(adc_pin)

        # 11 dB attenuation means full 0 - 3.3V range
        adc.atten(adc.ATTN_11DB)

        # Read ADC and convert to voltage
        val = adc.read()
        val = val * (3.3 / 4095) * 2 #Multiplied by 2 because there is 1:2 voltage divider on Tcell
        return round(val, 2)
    def status_signal(self, status):
        import time
        from machine import Pin
        led=Pin(21,Pin.OUT)        #create LED object from pin2,Set Pin2 to output

        led_state = 0
        if status == 'error':
            for i in range(20):
                led_state = 1 - led_state   # Toggle between 0 and 1 
                led.value(led_state)        #Set led turn on
                time.sleep(0.1)
        elif status == 'initializing':
            for i in range(6):
                led_state = 1 - led_state   # Toggle between 0 and 1 
                led.value(led_state)        #Set led turn on
                time.sleep(0.5)
        elif status == 'online':
            led.value(1)
            time.sleep(0.2)
            led.value(0)
        else:
            warning('Requested status signal not implemented on TTGO T-Cell HW!')
def test_display_engine():
    display = display_engine()
    display.text('Row 1',0)
    display.text('Row 2',1)
    display.text('Row 3',2)
    display.text('Row 4',3)

if __name__ == '__main__':
    tcell = tcell_engine()
    tcell.read_battery_voltage()