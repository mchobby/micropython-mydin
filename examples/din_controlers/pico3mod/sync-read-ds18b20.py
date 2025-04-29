# Test the basic features of DinControler Class
#  * test mydin.configure()
#  * test DS18B20 onewire temperature sensor reading
# 
# Hardware Configuration; DINCASE-2R-BP3MOD (2 relays backplane) + DINCASE-PICO-3MOD (Pico 2 Wireless MidBoard) 
# 
# See project: http://github/mchobby/micropython-mydin
#
from mydin import configure
from mydin.pico import Pico3Mod
from mydin.backplane.relays import TwoRelay3Mod 
import time, sys

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )


# === OneWire bus & DS18B20 ===================
print("OneWire & DS18B20")
_roms = din.onewire_roms
for txt in _roms:
	print( " Detected ROM:", txt )
if len(_roms)==0:
	print( " No ROM detected!")
print( " Has DS18B20:", din.has_ds18b20 )
print( " Temp : %f °C" % din.temp_ds18b20 )
print( " Temp : %f °C" % din.temp_ds18b20 )

