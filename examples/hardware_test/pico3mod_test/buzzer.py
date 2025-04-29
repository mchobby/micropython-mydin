""" dincase-mb3pico - test the buzzer """

from machine import Pin, PWM
from micropython import const
import time

DO = const(261) # Do
RE = const(294) # Ré
MI = const(329) # Mi
FA = const(349) # Fa
SOL= const(392) # Sol
LA = const(440) # La
SI = const(493) # Si
DO2= const(523) # Do

class Buzzer():
	def __init__(self, buz_pin ):
		self._pin = Pin( buz_pin, Pin.OUT )
		self._pwm = PWM( self._pin )
		self._pwm.freq( 3000 )
		self._pwm.duty_u16( 0 )

	def tone( self, freq=0 ):
		""" Play a tone at a given frequency. Frequency = 0 for silent """
		if freq == 0:
			self._pwm.duty_u16( 0 )
		else:
			self._pwm.freq( freq )
			self._pwm.duty_u16( 19660 ) # 30%

	def note( self, freq, duration ):
		""" duration in ms (float allowed) """
		# Note to freq
		self.tone( freq )
		# duration in microsecond (1=1000micros, 2=2000micros, etc)
		time.sleep_us( int(duration * 1000) ) # temps en micro-second

	def stop( self ):
		self.tone(0)

bz = Buzzer( Pin.board.GP13 )
for note in [DO,RE,MI,FA,SOL,LA,SI,DO2]:
	bz.note( note, 500 )
bz.stop()
time.sleep(1)
bz.tone( 3000 ) # 3 KHz Sound is very unpleasant
time.sleep(1)
bz.stop()
