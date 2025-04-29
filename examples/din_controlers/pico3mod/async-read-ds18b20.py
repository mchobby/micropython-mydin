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
import time, sys, asyncio

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )

counter = 0

# === OneWire bus & DS18B20 ===================
# When running DinControler asynchronously, a task 
# is created to capture the DS18B20 temperature! 
# The AsyncIO task is scheduled every  60 seconds 
# (see pico.py; DS18B20_UPDATE_TIME)

async def loop( din ):
	""" called again and again (like Arduino) """
	global counter
	counter += 1
	# Note, value may be null before first reading
	print( "iteration %3i : %s °C" % (counter, din.temp_ds18b20) )
	await asyncio.sleep( 5 )


din.setup( setup=None, loop=loop )
din.run()