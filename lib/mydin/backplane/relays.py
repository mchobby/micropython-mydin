from machine import Pin

class TwoRelay3Mod():
	def __init__( self ):
		self.out1 = None
		self.out2 = None

	@property
	def rel1( self ):
		return self.out1

	@property
	def rel2(self):
		return self.out2

	@property
	def relays(self):
		return [self.out1,self.out2]
	

	def attach( self, controler ):
		""" Attach the TwoRelay behaviours on controler """
		# Configure the Backplane interface
		self.out1 = Pin( controler.OUT1, Pin.OUT )
		self.out2 = Pin( controler.OUT2, Pin.OUT )
		setattr( controler, "out1", self.out1  )
		setattr( controler, "out2", self.out2 )

		# define properties for relay
		#rel1 = property( fget=_get_rel1, fset=None, fdel=None, doc="Relay 1" )
		setattr( controler, "rel1", self.rel1 )
		setattr( controler, "rel2", self.rel2 )
		setattr( controler, "relays", self.relays )
