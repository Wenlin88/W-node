import config
import network
import time
import urequests


import ulogger
import wnode.logging_handlers

logger = ulogger.Logger(__name__, wnode.logging_handlers.default_handlers())
debug = logger.debug
info = logger.info
warning = logger.warn
error = logger.error
critical = logger.critical




class wifi_engine():
    def __init__(self) -> None:
        pass
    def connect(self, ssid = None, pwd = None):
        if ssid is None:
            ssid = config.SSID
            pwd = config.wifi_passwd
        info(f'--- Connecting to {ssid}... ---')
        
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            
            sta_if.active(True)
            sta_if.connect(ssid, pwd)
            retry_count = 0
            max_retry_count = 10
            retry_wait_time = 1
            print(f'Please wait.',end="")
            while not sta_if.isconnected():
                if retry_count < max_retry_count:
                    print(f'.',end="")
                    time.sleep(retry_wait_time)
                    retry_count += 1
                else:
                    error('WiFi unreachable!')
                    sta_if.active(False)
                    return False # Tästä syystä voisi myös nostaa ihan virheenkin. Katsotaanko onko siitä mitään hyötyä, että ohjelma pysyy vielä suorituskykyisenä
            print('')
            info(f'Connected to Wifi')
            debug(sta_if.ifconfig()[0])
            self.ip = sta_if.ifconfig()[0]
            
        connected = self.check_internet_connection()
        self.wlan = sta_if
        if connected:
            info(f'--- Connected to internet! ---')
            return True
        else:
            warning('Connection to wifi ok but no internet connection!!')
            return False
    def check_internet_connection(self):
        response = urequests.get("http://clients3.google.com/generate_204")
        if response.status_code == 204:
            self.status = 'online'
            info("Internet status: online")
            return True
        elif response.status_code == 200:
            self.status = 'portal'
            info("Internet status: portal")
            return False
        else:
            self.status = 'offline'
            info("Internet status: offline")
            return False
    def scan_wlan_networks(self):
        sta_if = network.WLAN(network.STA_IF)
        info('--- Scanning for WLAN networks...  ---')
        sta_if.active(True)
        scan_result = sta_if.scan()
        
        number_of_found_networks = len(scan_result)
        info(f'{number_of_found_networks} networks found!')
        info(f'No \t RSSI \t Name')
        for i, result in enumerate(scan_result):
            info(f'{i} \t {result[3]} \t {result[0].decode()} ')
        sta_if.active(False)
        info('--- End of scan  ---')    



if __name__ == '__main__':
    we = wifi_engine()
    we.connect()
        