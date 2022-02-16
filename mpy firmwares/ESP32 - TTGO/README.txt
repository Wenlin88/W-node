Lataa firmis kehityslaudalle seuraavasti -->
esptool --chip esp32 --port COM3 --baud 105200 write_flash -z 0x1000 esp32-20220117-v1.18.elf
