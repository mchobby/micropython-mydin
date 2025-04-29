# Pico based controler boards for MyDin 
#
from .controler import DinControler, format_rom
from .buzzer import Buzzer
from machine import Pin, I2C, RTC, ADC, reset, WDT
from pca9536 import PCA9536
from ds3231 import DS3231
from onewire import OneWire
from ds18x20 import DS18X20
import time, asyncio
import micropython
micropython.alloc_emergency_exception_buf(100)

RUN_APP_PIN = Pin.board.GP3  # High=Run, Low=Stop

DEBOUNCE_MS = 300 # Time between multiples buttons activation
DS18B20_UPDATE_TIME = 10 # ASYNC seconds timing between 2 temperature acquisition
MONITOR_TIME = 60 # ASYNC seconds timing between 2 monitoring checks
OVER_TEMP = 75 # Over-temperature 

class PicoControler( DinControler ):
	#=== Immuable definition between Pico controlers ===
	OUT1 = Pin.board.GP16 # Backplace interface
	OUT2 = Pin.board.GP17
	OUT3 = Pin.board.GP18
	IN1  = Pin.board.GP27
	A1   = Pin.board.GP27
	IN2  = Pin.board.GP19

	SDA  = Pin.board.GP6 # I2C(1) - Qwiic/UEXT
	SCL  = Pin.board.GP7

	MISO = Pin.board.GP8 # SPI(1) - UEXT
	MOSI = Pin.board.GP11
	SCK  = Pin.board.GP10
	CSN  = Pin.board.GP9

	RX   = Pin.board.GP5 # UART(1) - UEXT
	TX   = Pin.board.GP4

	STATUS = Pin.board.GP14 # Status LED


	def __init__( self, BackplaneClass ):
		super().__init__( BackplaneClass, RUN_APP_PIN )
		self.status = Pin( PicoControler.STATUS, Pin.OUT )
		self.status.on()
		self.i2c = I2C( 1, sda=PicoControler.SDA, scl=PicoControler.SCL, freq=400000 )
		self.mcu_rtc = RTC()
		self.adc4 = ADC(4)
		self.wdt = None

	@property
	def internal_temperature( self ):
		# Read Pico Internal temperature
		value = self.adc4.read_u16()
		volt = value * (3.3 / 65535.0)
		celsius = 27 - (volt - 0.706) / 0.001721
		return celsius

	# Pico WatchDog (override)
	def setup_watchdog( self, time_ms ):		
		self.wdt = WDT( timeout=time_ms )

	# Pico WatchDog (override)
	def feed_watchdog( self ):
		if self.wdt:
			self.wdt.feed()

class PcaPinAdapter():
	""" Make a PCA bit acting as a Pin """
	def __init__( self, owner_pca, bit, value=False ):
		assert 0<=bit<=3
		self.pca = owner_pca
		self.bit = bit
		self.state = None # Last known pin state
		self.value( value )

	# Mimic a Pin interface
	def on(self):
		self.value(True)

	def off(self):
		self.value(False)

	def value( self, value=None ):
		if value== None:
			return self.state 
		else:
			self.pca.output( self.bit, value )
			self.state = value

	def toggle( self ):
		self.value( not(self.state) )


class Pico3Mod( PicoControler ):
	BTN1 = Pin.board.GP20
	BTN2 = Pin.board.GP21
	BTN3 = Pin.board.GP22
	BTN4 = Pin.board.GP26

	def __button_handler( self, p ):
		# which button
		for i in range( len(self.__buttons) ):
			if (p == self.__buttons[i]) and (self.__pressed[i]==None):
					self.__pressed[i]=time.ticks_ms()
					break


	""" Pico controler for DINCASE 3 modules """
	def __init__( self, BackplaneClass ):
		super().__init__( BackplaneClass )
		self.buzzer = Buzzer( Pin.board.GP13 )
		# User LEDs controler
		self.pca = PCA9536( self.i2c )
		for pin in range(4):
			self.pca.setup( pin, Pin.OUT )
			self.pca.output( pin, False )
		self.pca.output(0, True ) # One LED = PCA initialized

		# Make the LEDs acting as Pin class
		self.led0 = PcaPinAdapter( self.pca, 0 ) 
		self.led1 = PcaPinAdapter( self.pca, 1 ) 
		self.led2 = PcaPinAdapter( self.pca, 2 ) 
		self.led3 = PcaPinAdapter( self.pca, 3 ) 

		# MCU clock initialization
		self.ext_rtc = DS3231( self.i2c )
		_time = self.ext_rtc.datetime()
		self.mcu_rtc.datetime( _time )
		self.pca.output(1, True ) # Two LED = RTC initialized
		# Current time
		print( "mcu localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*self.mcu_rtc.datetime()) )

		# OneWire bus scan
		self.onewire = OneWire( Pin.board.GP15 )
		self.roms = self.onewire.scan()
		# get the first ROM for DS18B20 (familly 28)
		self.rom_ds18b20 = None
		for _rom in self.roms:
			if _rom[0] == 0x28:
				self.rom_ds18b20 = _rom
				break
		self._ds18b20 = None # created @ first access
		self.__async_temp_ds18b20 = None # temp value collected by asynchronous 
		self.pca.output(2, True ) # Tree LED = OneWire initialized

		# Input buttons callback
		self.__buttons = [] # Buttons reference
		self.__pressed = [] # Last Ticks_ms pressed
		self.debounce_ms = DEBOUNCE_MS # Button debounce time
		for pin in ( Pico3Mod.BTN1, Pico3Mod.BTN2, Pico3Mod.BTN3, Pico3Mod.BTN4 ):
			self.__buttons.append( Pin( pin, Pin.IN, Pin.PULL_UP ) )
			self.__buttons[len(self.__buttons)-1].irq( self.__button_handler, Pin.IRQ_FALLING )
			self.__pressed.append( None )

		# Reset all
		[ self.pca.output( idx, False ) for idx in range(0,4) ]
		self.status.off()
		self.buzzer.note( 5000, 250 )
		self.buzzer.stop()


	def before_run( self ):
		_r = super().before_run()
		if not _r:
			return _r
		# === Check startup condition ===
		print( "Over-temperature set %s °C" % OVER_TEMP )
		_t = self.internal_temperature 
		if _t > OVER_TEMP:
			print( "Over temperature %s °C reached (current: %s °C)" % (OVER_TEMP,_t) )
			return False # do not allow running the software
		# Allow startup
		return True 


	async def __coro_ds18b20( self ):
		if self._ds18b20==None:
			self._ds18b20 = DS18X20( self.onewire )
		while True:
			self._ds18b20.convert_temp()
			await asyncio.sleep_ms( 750 )
			self.__async_temp_ds18b20 = self._ds18b20.read_temp( self.rom_ds18b20 )
			await asyncio.sleep( DS18B20_UPDATE_TIME )


	async def __coro_monitor( self ):
		# Just monitor the internals of the din controler
		while True:
			_t = self.internal_temperature 
			print( "Monitor: %s °C" % _t )
			if _t > OVER_TEMP:
				print( "Over temperature %s °C reached (current: %s °C)" % (OVER_TEMP,_t) )
				reset()
			await asyncio.sleep( MONITOR_TIME )	


	def tasks_setup( self, async_evloop ):
		super().tasks_setup( async_evloop )
		if self.has_ds18b20:
			print( 'Create ds18b20 task...' )
			async_evloop.create_task( self.__coro_ds18b20() )
		print( 'Create monitor task...' )
		async_evloop.create_task( self.__coro_monitor() )


	@property
	def leds( self ):
		return [self.led0,self.led1,self.led2,self.led3]

	@property
	def buttons( self ):
		return self.__buttons

	@property 
	def onewire_roms( self ):
		""" returns the OneWire ROMs as Human Redeable entries """
		return [format_rom(_rom) for _rom in self.roms ]

	@property
	def has_ds18b20(self):
		return self.rom_ds18b20 != None


	@property
	def temp_ds18b20(self):
		""" Read the temperature of first DS18B20 or 0°C. (blocking read for 750ms) """
		if self.rom_ds18b20 == None:
			return 0.0
		
		if self.is_async:
			# value obtained via asynchronous tasks __coro_ds18b20
			return  self.__async_temp_ds18b20 
		else:
			#
			if self._ds18b20==None:
				self._ds18b20 = DS18X20( self.onewire )
			self._ds18b20.convert_temp()
			time.sleep_ms( 750 )
			return self._ds18b20.read_temp( self.rom_ds18b20 )

	def was_pressed( self, idx ):
		""" check if a button has pressed then Reset the flag (0 indexed)"""
		_r = (self.__pressed[idx]!=None) and (time.ticks_diff(time.ticks_ms(), self.__pressed[idx])>=self.debounce_ms )
		if _r:
			self.__pressed[idx] = None # Reset the flag
		return _r

