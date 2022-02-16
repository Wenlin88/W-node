Lataa firmis kehityslaudalle seuraavasti -->
esptool --chip esp32 --port COM3 erase_flash
esptool --chip esp32 --port COM3 --baud 105200 write_flash -z 0x1000 M5STACK_ATOM-20220117-v1.18.bin

Huom! 
Jotta sain firmiksen lataamisen toimivaan piti baudrate pudottaa alaspäin

Huom2! 
M5 stack firmiksellä ei ollut valmiina MQTT clienttiä, mutta sen pystyi asentamaan seuraavasti --> https://pypi.org/project/micropython-umqtt.simple2/ --> Suorita seuraava M5Atomin terminaalissa
	import upip
	upip.install("micropython-umqtt.simple2")
