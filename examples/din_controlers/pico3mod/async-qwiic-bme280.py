# Test DinControler qwiic connector (I2C bus)
#  * load bme280 library

#  * display internal temperature (Pico) onto SpakFun SerLCD LCD-16398
# 
# Hardware Configuration:
#  * DINCASE-2R-BP3MOD (2 relays backplane) + DINCASE-PICO-3MOD (Pico 2 Wireless MidBoard) 
#  * SpakFun SerLCD (LCD-16398) 20x4, I2C @ 0x68
# 
# See project: http://github/mchobby/micropython-mydin
# SerLCD MicroPython Library: https://github.com/mchobby/esp8266-upy/tree/master/qwiic-serlcd-i2c
#
from mydin import configure
from mydin.pico import Pico3Mod
from mydin.backplane.relays import TwoRelay3Mod 
import time, sys

from bme280 import *

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )

def setup( din ):
	# Add a new attribute to "din" instance
	din.sensor = BME280( i2c=din.i2c, address=BMP280_I2CADDR )
	din.last_update = time.ticks_add( time.ticks_ms(), -11000 ) # Last update outdated
	din.rel1.off()

async def loop( din ):
	""" called again and again (like Arduino) """

	# Update LCD once every 5 seconds
	if time.ticks_diff( time.ticks_ms(), din.last_update )>10000:
		# temperature (celcius), atmospheric_pressure (hPascal), Relative_humidity (percent)
		temp, hpa, rh = din.sensor.raw_values
		# Activate FAN (relay 1) if temp > 25°C
		din.rel1.value( temp>25 )
		print( "temperature",temp, "pressure", hpa, "humidity", rh, "Rel1 is %s" % ("ON" if din.rel1.value() else "off")   )

		din.last_update = time.ticks_ms()



din.setup( setup=setup, loop=loop )
din.run()

if din.loop_exception != None:
	print( "An error %s occured!" % (din.loop_exception.__class__.__name__ ) )
	print( "with message: %s" % din.loop_exception )

