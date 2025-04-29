from machine import Pin
from binascii import hexlify
import asyncio

LOOP_TIME_MS = 20 # pause between two consecutive loop call

class DinControler():
	def __init__( self, BackplaneClass, RunApp_pin ):
		self.backplane = BackplaneClass()
		self.__setup = None # sync function
		self.__loop  = None # AsyncIO function : user script code to execute again and again
		self.__tasks = None # sync function : allow user script to insert tasks in the AsyncIO Event Loop
		self.is_async = False # set to True when asynchronous run is started (see run)
		self.__run_app = Pin( RunApp_pin, Pin.IN, Pin.PULL_UP )
		self.loop_exception = None
		self.loop_time_ms   = LOOP_TIME_MS


	def setup( self, setup=None, loop=None, on_tasks_create=None ):
		assert loop!=None
		self.__setup = setup  
		self.__loop = loop    
		self.__ontasks = on_tasks_create

	# Must be override for implementation
	def setup_watchdog( self, time_ms ):		
		pass

	# Must be override for implementation
	def feed_watchdog( self ):
		pass

	async def __coro_userloop( self ):
		# Run the user 'async def loop()' again and again
		self.loop_exception = None
		try:
			while True:
				await self.__loop( self )
				self.feed_watchdog()
				await asyncio.sleep_ms( self.loop_time_ms )
		except Exception as e:
			self.loop_exception = e # remember the exception
			print( "[ERROR] %s: %s in loop(). Exit!" % (e.__class__.__name__, e) )
			raise

	async def __run_app_exit( self ):
		""" fin d'execution lorsque quitte la fonction """
		while (self.__run_app.value()==True) and (self.loop_exception==None):
			await asyncio.sleep( 3 )
		print( "[EXIT] run app exit!" )
		return
		

	def tasks_setup( self, async_evloop ):
		# Made overidable for descdant class
		print( "USER Loop Setup..." )
		loop_task = async_evloop.create_task( self.__coro_userloop() )
		# Allow user define script to register its own tasks
		if self.__ontasks != None:
			print( "USER Tasks Setup..." )
			self.__ontasks( async_evloop ) 

	def before_run( self ):
		print( "%s.before_run() entering..." % self.__class__.__name__ )
		return True

	def after_run( self ):
		pass

	def run( self ):
		""" Asynchronous execution """
		if self.__run_app.value()==False:
			print( "[EXIT] %s.run() because run app exit!" % self.__class__.__name__ )
			return 

		if not self.before_run():
			print( "[EXIT] before_run() abort!" )
			return


		print( "%s.run() entering..." % self.__class__.__name__ )
		self.is_async = True

		# Additionnal USER Hardware Setup
		if self.__setup != None:
			print( "USER Hardware Setup..." )
			self.__setup(self)

		async_evloop = asyncio.get_event_loop()

		# Run the USER loop and other tasks
		self.tasks_setup( async_evloop )
		print( "running event_loop..." )
		#async_evloop.run_forever() 
		async_evloop.run_until_complete( self.__run_app_exit() )
		print( "event_loop ended!" )
		self.after_run()


def format_rom( buffer ):
	""" Format the OneWire ROM addr """
	_s = hexlify(buffer).decode('ASCII').upper()
	_l = [_s[i:i+2] for i in range(0, len(_s), 2)]
	return ':'.join( _l )	