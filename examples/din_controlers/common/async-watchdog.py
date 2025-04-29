# Test the basic features of DinControler Class
#  * test mydin.configure()
#  * test mydin.setup_watchdog()
#  * test mydin.feed_watchdog()
#  
# Loop execution must be below watchdog timeout. When timeout is reach then the MCU resets.
# 
# How to test: keep the button1 pressed long time enough to keeps the loop() reaching the timeout
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
	din.leds[0].off()
	# direct access to button state
	while din.buttons[0].value()==0: # while pressed
		din.leds[0].on()


din.setup( setup=None, loop=loop )
# Watchdog resets if loop() stay locked for 2 sec 
din.setup_watchdog( 2000 ) 
din.run()


