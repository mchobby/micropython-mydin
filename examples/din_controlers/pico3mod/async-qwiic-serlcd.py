# Test DinControler qwiic connector (I2C bus)
#  * load serlcd library
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

from serlcd import SerLCD

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )

def setup( din ):
	# Add a new attribute to "din" instance
	din.lcd = SerLCD( din.i2c, cols=16, rows=4 )
	din.lcd.backlight( (0,0,255) ) # Blue
	din.lcd.set_cursor( (7,1) ) # column,line (0 à N-1)
	din.lcd.print( "MyDin" )
	din.lcd.set_cursor( (3,2) ) # column,line (0 à N-1)
	din.lcd.print( "by MCHobby.be")
	din.lcd_last_update = time.ticks_ms()

async def loop( din ):
	""" called again and again (like Arduino) """

	# Update LCD once every 5 seconds
	if time.ticks_diff( time.ticks_ms(), din.lcd_last_update )>5000:
		din.lcd.clear()
		din.lcd.print("Internal Temp:" )
		din.lcd.set_cursor( (3,1) )
		din.lcd.print( "%2.2f C" % din.internal_temperature )
		din.lcd_last_update = time.ticks_ms()



din.setup( setup=setup, loop=loop )
din.run()

if din.loop_exception != None:
	print( "An error %s occured!" % (din.loop_exception.__class__.__name__ ) )
	print( "with message: %s" % din.loop_exception )

