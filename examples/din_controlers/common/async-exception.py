# Test reaction of DinControler Class when exception occurs
#  * test mydin.configure()
#  * test button press (button 2 raise an exception)
# 
# Hardware Configuration; DINCASE-2R-BP3MOD (2 relays backplane) + DINCASE-PICO-3MOD (Pico 2 Wireless MidBoard) 
# 
# See project: http://github/mchobby/micropython-mydin
#
from mydin import configure
from mydin.pico import Pico3Mod
from mydin.backplane.relays import TwoRelay3Mod 
import time, sys

class KaboomError( Exception ):
	pass

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )

async def loop( din ):
	""" called again and again (like Arduino) """
	for i in range( 4 ): # 0..3 = 4 buttons
		if din.was_pressed( i ):
			din.leds[i].toggle()
			# raise en exception is button 2 is pressed
			if i==1: 

				# Exceptions under asynchio tasks doesn't halt the EventLoop
				# However when an exception occurs in the the mainloop, that
				# one will exit the eventloop (terminate din.run() ) within 
				# the 3 seconds. Exeption instance is available via the 
				# loop_exception property.
				# 
				raise KaboomError( "This exception will exits the code")


din.setup( setup=None, loop=loop )
din.run()
print( "="*40 )
print( "din.run() did exit!!!")

if din.loop_exception != None:
	print( "An error %s occured!" % (din.loop_exception.__class__.__name__ ) )
	print( "with message: %s" % din.loop_exception )

