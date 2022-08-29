import time
import machine
from umqtt.simple import MQTTException
import gc
import wnode
import wnode.wifi as wifi
import wnode.mqtt as mqtt
import wnode.ha as ha
import wnode.ble as ble
import ubinascii
import math


def memory_usage_check(msg) -> None:
    print(msg)
    print('Allocated: ' + str(gc.mem_alloc()))
    print('Free: ' + str(gc.mem_free()))


import ulogger
import wnode.logging_handlers

logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical


# Internal functions
def highlighted_info(msg):
    fill_string_size = len(msg)
    info("-" * fill_string_size)
    info(msg)
    info("-" * fill_string_size)
    
class wnode_engine():
    device_type = "ESP32"
    manufacturer =  "Henri Wenlin"
    sw_version = wnode.__version__

    def __init__(self, friendly_name, params = {}):
        self.friendly_name = friendly_name + ' ' + ubinascii.hexlify(machine.unique_id()).decode()
        highlighted_info(f"--- {self.friendly_name} initialization in progress... ---")
        
        self.hw_type = None
        self.wifi = None
        self.mqtt = None
        self.ha = None
        self.ble = None
        self.status = 'initializing'
        self.retry_count = 0
        
        if 'hw_type' in params:
            self.hw_type = params['hw_type']
            if self.hw_type == 'TTGO display':
                self._init_ttgo_display()
            elif self.hw_type == 'Atom matrix':
                import wnode.m5stack as m5
                self.device = m5.atom_matrix()
                self.device.status_signal('initializing')
                info('M5stack Atom Matrix hardware initialized!')  
            elif self.hw_type == 'TTGO T-cell':
                import wnode.ttgo as ttgo
                self.device = ttgo.tcell()
                self.device.status_signal('initializing')
                info('TTGO T-cell hardware initialized!')  
        else:
            info('HW type not defined. Trying to auto identify...')
            import uos
            mach_info = uos.uname()
            debug(mach_info)
            if mach_info.machine == 'M5Stack ATOM with ESP32-PICO-D4':
                info('Atom found! Identification between Lite and Matrix missing. This is in todo. This could be done by for example detecting if there is MPU6886 or not....')
            elif mach_info.machine == 'TTGO T-Display with ESP32':
                info('TTGO display found')
                self._init_ttgo_display()
        if 'wifi' in params:
            if params['wifi'] == True:
                info('Initializing wifi...')
                
                self.wifi =  wifi.wifi_engine()
                self.connect_to_wifi = self.wifi.connect
                self.check_internet_connection = self.wifi.check_internet_connection
                
                connection = False
                while not connection:
                    connection = self.connect_to_wifi()
                    if connection:
                        self.status = 'online'
                    else:
                        if self.retry_count < 5:
                            warning('WiFi connection failed. Retrying after 10sec...')
                            self.status = 'error'
                            time.sleep(10)
                        else:
                            error('Too many retries for WiFi connection. HW reset activated...')
                            machine.reset()

                if not self.hw_type == None:
                    self.status_update() 

            else:
                debug('WiFi disabled')
        if 'mqtt' in params:
            if params['mqtt'] == True:
                info('Initializing mqtt...')
                self.mqtt = mqtt.mqtt_engine()

                connection = self.mqtt.connect(ssl = False)
                if connection:
                    self.status = 'online'
                    info('MQTT initialization done!')
                else:
                    error('MQTT connection failed! Resetting after 30sec...')
                    self.status = 'error'
                    time.sleep(30)
                    machine.soft_reset()

                if not self.hw_type == None:
                    self.status_update()
            else:   
                debug('MQTT disabled')
        if 'homeassistant' in params:
            if params['homeassistant'] == True:
                info('Doing HA introduction for ' + friendly_name)
                if self.mqtt != None:
                    if self.mqtt.status == 'online':
                        self.ha = ha.ha_engine(self.mqtt.client)
                        status = self.ha.introduce_wnode_to_ha(self.friendly_name, self.device_type, self.hw_type, self.manufacturer, self.sw_version)
                        if status:
                            info('HA introduction successful!')
                            self.status = 'online'
                        else:
                            error('HA introduction failed! Resetting after 30sec...')
                            self.status = 'error'
                            time.sleep(30)
                            machine.soft_reset()

                        if not self.hw_type == None:
                            self.status_update()
                    else:
                        warning("MQTT client not online. Home assistant initialization can't continue")
                else:
                    warning("MQTT not initialized. Home assistant initialization can't continue")
            else:
                debug('MQTT disabled')
        if 'ble' in params:
            if params['ble'] == True:
                info('Enabling Bluetooth for W-node')
                self.ble = ble.ble_engine()
                info('Bluetooth enabled')
            else:
                debug('Bluetooth disabled')

        highlighted_info(f"--- {self.friendly_name} initialized! ---") # Initialization completed message
    def run_ble_beacon_scan_app(self, cycle_time = 6, scan_time = 5):
        while True:
            gc.collect()
            self.status = 'scanning'
            self.status_update()
            time.sleep(0.1)
            self.scan_ble_beacons(scan_time)
            time.sleep(0.1)
            self.status_update()
            time.sleep(cycle_time-scan_time)
    def scan_ble_beacons(self, scan_time = 5):
        if self.wifi.check_internet_connection():
            info(f'Scanning for Bluetooth devices for {scan_time}s...')
            self.ble.scan(scan_time = scan_time)
            beacon_data = self.ble.search_beacons_from_scan_results()
            number_of_beacons_found = len(beacon_data)
            info(f'{number_of_beacons_found} beacons found.')
            info('Publishing beacon data to HA...')
            self.ha.publish_ble_beacon_data(beacon_data)
            info('Scan done')
            self.retry_count = 0
            self.status = 'online'
        else:
            connection = False
            while not connection:
                connection = self.wn.wifi.connect()
                if self.retry_count < 100 and connection:
                    warning('No connection to WiFi. Retrying after 10s...')
                    self.retry_count += 1
                    time.slepp(10)
                else:
                    warning('Two many reconnect attempts to wifi! Restarting..')
                    machine.reset()
            self.retry_count = 0
            self.status = 'online'
    def run_temperature_scan_app(self, cycle_time = 5):
        import wnode.ds18b20 as ds18b20
        ds = ds18b20.engine(display = self.display, friendly_name = self.friendly_name, mqtt_client = self.mqtt.client)
        ds.init_DS18B20_measurement(25)
        while True:
            if self.wifi.check_internet_connection():
                gc.collect()
                time.sleep(0.1)
                ds.read_DS18B20_measurement()
                time.sleep(0.1)
                self.status_update()
                time.sleep(cycle_time)
                info('Scan done')
                self.retry_count = 0
                self.status = 'online'
            else:
                connection = False
                while not connection:
                    connection = self.wn.wifi.connect()
                    if self.retry_count < 100 and connection:
                        warning('No connection to WiFi. Retrying after 10s...')
                        self.retry_count += 1
                        time.sleep(10)
                    else:
                        warning('Two many reconnect attempts to wifi! Restarting..')
                        machine.reset()
                self.retry_count = 0
                self.status = 'online'  
    def run_temperature_scan_app2(self, cycle_time = 5):
        self.device.init_adc()
        self.ha.introduce_new_measurement_to_exsitsting_sensor('Temperature', self.friendly_name, unit = "°C")
        while True:
            if self.wifi.check_internet_connection():
                gc.collect()
                time.sleep(0.1)
                u1 = self.device.read_adc()
                r2 = 100e3
                vtot = 3.35
                r1 = u1*r2/(vtot-u1)
                debug(f'Resistance: {r1}')
                t = 1/(1/(25+273.15)-math.log(32762/r1)/4300)-273.15
                info(f'Temperature: {t}')
                self.ha.publish_measurement('Temperature', self.friendly_name, t)
                time.sleep(0.1)
                self.status_update()
                time.sleep(cycle_time)
                info('Scan done')
                self.retry_count = 0
                self.status = 'online'
            else:
                connection = False
                while not connection:
                    connection = self.wn.wifi.connect()
                    if self.retry_count < 100 and connection:
                        warning('No connection to WiFi. Retrying after 10s...')
                        self.retry_count += 1
                        time.sleep(10)
                    else:
                        warning('Two many reconnect attempts to wifi! Restarting..')
                        machine.reset()
                self.retry_count = 0
                self.status = 'online'   
    
    def run_tcell_app(self, cycle_time = 5):
        self.ha.introduce_new_measurement_to_exsitsting_sensor('battery_voltage',self.friendly_name)
        while True:
            if self.wifi.check_internet_connection():
                gc.collect()
                time.sleep(0.1)
                bat_volt = self.device.read_battery_voltage()
                self.ha.publish_measurement('battery_voltage', self.friendly_name, bat_volt)
                time.sleep(0.1)
                self.status_update()
                time.sleep(cycle_time)
                info('Scan done')
                self.retry_count = 0
                self.status = 'online'
            else:
                connection = False
                while not connection:
                    connection = self.wn.wifi.connect()
                    if self.retry_count < 100 and connection:
                        warning('No connection to WiFi. Retrying after 10s...')
                        self.retry_count += 1
                        time.sleep(10)
                    else:
                        warning('Two many reconnect attempts to wifi! Restarting..')
                        machine.reset()
                self.retry_count = 0
                self.status = 'online'
    def status_update(self):
        if self.hw_type == 'TTGO display':
            self.display.text(' '*15,1) # Flush old status text away
            self.display.text(f'status: {self.status}',1)
        elif self.hw_type == 'Atom matrix':
            self.device.status_signal(self.status)
        elif self.hw_type == 'TTGO T-cell':
            self.device.status_signal(self.status)
        else:
            warning('Device status indication method not set for this hw type...')
        
        if self.mqtt != None and self.ha != None:
            self.mqtt.client.connect()
            self.mqtt.client.publish(
                self.ha.wnode_uptime_topic,
                msg=str(time.ticks_ms()/1000).encode(),
                qos = 0)
            self.mqtt.client.disconnect()

    
    # Mics  
    def install_mqtt_simple():
        import upip
        upip.install('umqtt.simple')
    
    # Internals
    def _init_ttgo_display(self):
        import wnode.ttgo as ttgo
        display = ttgo.display_engine()
        display.text(self.friendly_name, 0)
        display.text(f'status: {self.status}',1)
        self.display = display
        self.hw_type = 'TTGO display'
        info('TTGO Display hardware initialized!')
if __name__ is "__main__":
    wnode_parameters = {
    'hw_type': 'Atom matrix',
    'wifi': True,
    'mqtt': True,
    'homeassistant': True,
    'ble': 0,
    'DS18B20': False,
    }
    wn = wnode_engine('W-Node', wnode_parameters)
