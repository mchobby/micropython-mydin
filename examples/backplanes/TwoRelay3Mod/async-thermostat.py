# Create an enhanced Thermostat controler with DinControler Class
#  * DS18B20 is connected to 1Wire port
#  * Rel 1 control the Heater
#  * LED 1 reflect the Rel 1 state.
#
# 
# Hardware Configuration; DINCASE-2R-BP3MOD (2 relays backplane) + DINCASE-PICO-3MOD (Pico 2 Wireless MidBoard) 
# 
# See project: http://github/mchobby/micropython-mydin
#
from mydin import configure
from mydin.pico import Pico3Mod
from mydin.backplane.relays import TwoRelay3Mod 
from hyst import HeaterTh
import time, sys, asyncio

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )
thermostat = HeaterTh( 25, 2 ) # Thermostat

# === OneWire bus & DS18B20 ===================
# When running DinControler asynchronously, a task 
# is created to capture the DS18B20 temperature! 
# The AsyncIO task is scheduled every  60 seconds 
# (see pico.py; DS18B20_UPDATE_TIME)

async def loop( din ):
	""" called again and again (like Arduino) """
	global thermostat
	if din.temp_ds18b20==None:
		await asyncio.sleep( 2 )
		return

	heat = thermostat.update( din.temp_ds18b20 )
	din.led0.value( heat )
	din.rel1.value( heat )
	# Note, value may be null before first reading
	print( "%s °C" % (din.temp_ds18b20,) )
	await asyncio.sleep( 2 )


din.setup( setup=None, loop=loop )
din.run()