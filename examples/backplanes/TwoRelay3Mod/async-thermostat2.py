# Create a very basic Thermostat controler with DinControler Class
#  * DS18B20 is connected to 1Wire port
#  * Rel 1 control the Heater
#  * LED 1 reflect the Rel 1 state.
#
#  * Button 1 invert (force) the state of the relay. 
#  * Forced state is canceled with the thermostat state reach the forced state
#  * Forced state is canceled when the button 2 is pressed.
#  * LED2 is lit while a forced state do applies
#  * button 3 will decrease the setpoint T°. Led 3 will blick once to acknowledge.
#  * button 4 will increase the setpoint T°. Led 4 will blink once to acknowledge.
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
forced = None # Forced state (High=True,Low=False,None=None)
last_print = 1

# === OneWire bus & DS18B20 ===================
# When running DinControler asynchronously, a task 
# is created to capture the DS18B20 temperature! 
# The AsyncIO task is scheduled every  60 seconds 
# (see pico.py; DS18B20_UPDATE_TIME)

async def loop( din ):
	""" called again and again (like Arduino) """
	global thermostat, forced, last_print
	if din.temp_ds18b20==None:
		await asyncio.sleep( 2 )
		return

	# User Force state change ?
	if din.was_pressed( 0 ):
		forced = not(din.rel1.value())


	# Ask to reset forced state ?
	if din.was_pressed( 1 ):
		forced = None

	# Increate / decrease setpoint
	if din.was_pressed( 2 ):
		thermostat.setpoint -= 1
		print( 'setpoint @ %i °C' % thermostat.setpoint )
		din.led2.on()
		await asyncio.sleep_ms( 300 )
		din.led2.off()
	if din.was_pressed( 3 ):
		thermostat.setpoint += 1
		print( 'setpoint @ %i °C' % thermostat.setpoint )
		din.led3.on()
		await asyncio.sleep_ms( 300 )
		din.led3.off()

	# IF forced THEN apply forced state
	if forced != None:
		heat = forced
		# Should we auto-reset the forced state
		if (forced == thermostat.update( din.temp_ds18b20) ):
			forced=None # Reset forced state

	# IF not forced THEN follow thermostat
	if forced==None: 
		heat = thermostat.update( din.temp_ds18b20 )
	
	din.led1.value( forced!=None )
	din.led0.value( heat )
	din.rel1.value( heat )

	# print status once every 2 seconds
	if time.ticks_diff( time.ticks_ms(), last_print )>2000:
		print( "[%s] %s °C - %s - %s" % (thermostat.setpoint, din.temp_ds18b20, "Heat" if heat else "...",  "(forced)" if forced!=None else "") )
		last_print = time.ticks_ms()

	await asyncio.sleep_ms( 100 )


din.setup( setup=None, loop=loop )
din.run()