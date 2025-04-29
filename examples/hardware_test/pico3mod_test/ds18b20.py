# """ dincase-mb3pico - Test the 1wire of connector """
#
# Shop: https://shop.mchobby.be/senseur-divers/259-senseur-temperature-ds12b20-extra-3232100002593.html
# Shop: https://shop.mchobby.be/senseur-divers/151-senseur-temperature-ds18b20-etanche-extra-3232100001510.html
#
from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20
from time import sleep_ms
from binascii import hexlify
import sys

bus = OneWire( Pin(Pin.board.GP15) )
ds = DS18X20( bus )

def format_rom( buffer ):
	_s = hexlify(rom).decode('ASCII').upper()
	_l = [_s[i:i+2] for i in range(0, len(_s), 2)]
	return ':'.join( _l )

# Scan all the DS12B20 on the bus (for each of the ROM address).
# Each of the device do have a specific address
roms = ds.scan()
if len(roms)==0:
	print( "Nothing detected on OneWire bus")
	sys.exit(1)

for rom in roms:
	print( "ROM", format_rom(rom) )

# Request temps from sensors
ds.convert_temp()
# Waits for 750ms (required)
sleep_ms( 750 )

# Display the temp for each device
for rom in roms:
	temp_celsius = ds.read_temp(rom)
	print( "Temp: %s Celcius" % temp_celsius )
