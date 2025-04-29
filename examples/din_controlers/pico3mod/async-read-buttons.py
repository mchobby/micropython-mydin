# Test the basic features of DinControler Class
#  * test mydin.configure()
#  * test button press
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

async def loop( din ):
	""" called again and again (like Arduino) """
	for i in range( 4 ): # 0..3 = 4 buttons
		if din.was_pressed( i ):
			din.leds[i].toggle()
			# Toggle the relays with
			# the first and second LEDs
			if 0<=i<=1: 
				din.relays[i].value( din.leds[i].value() )


din.setup( setup=None, loop=loop )
din.run()


