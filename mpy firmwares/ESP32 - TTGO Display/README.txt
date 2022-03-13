Lataa firmis kehityslaudalle seuraavasti -->
esptool --chip esp32 --port COM4 --baud 105200 write_flash -z 0x1000 esp32-20220117-v1.18.elf

Display tuki löytyy seuraavasta kirjastosta
https://github.com/russhughes/st7789_mpy/blob/master/firmware/T-DISPLAY-ESP32/firmware.bin
