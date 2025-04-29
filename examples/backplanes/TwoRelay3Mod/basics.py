# Test the basic features of DinControler Class
#  * test mydin.configure()
#  * test the hardware control
# 
# Hardware Configuration; DINCASE-2R-BP3MOD (2 relays backplane) + DINCASE-PICO-3MOD (Pico 2 Wireless MidBoard) 
# 
# See project: http://github/mchobby/micropython-mydin
#
from mydin import configure
from mydin.pico import Pico3Mod
from mydin.backplane.relays import TwoRelay3Mod 
import time

# Which Controler + Backplane to use
din = configure( Pico3Mod, TwoRelay3Mod )

# Get the RTC time
DAYS = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]
_time2 = din.mcu_rtc.datetime()
print( "mcu datetime :", _time2 )
print( "mcu time     : %s secs" % time.mktime(_time2) )
print( "mcu localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*_time2) )
print( 'Weekday      : %s' % DAYS[_time2[3]] )
print( '' )


print( "din :", din )
print( dir( din ) )

# === Relays ==================================
print( "" )
print( "Manipulate the relays" )
din.rel1.on()
print( "Rel1 is", din.rel1.value() )
time.sleep(1)

din.rel2.on()
print( "Rel2 is", din.rel2.value() )
time.sleep(1)

print( "All relays off" )
for relay in din.relays:
	relay.off()
print( "relays state", [relay.value() for relay in din.relays] )


# === LEDs ====================================
print("LEDs chaser")
for i in range( 20 ):
	for led in din.leds:
		led.toggle()
		time.sleep_ms(100)
# turn off all leds.
[ led.off() for led in din.leds ]

