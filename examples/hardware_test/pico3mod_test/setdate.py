""" dincase-mb3pico - Setting the external RTC datetime """
#
# When using
#    mpremote rtc --set
# THEN the MCU internal CPU is set to current computer date and time.
# So we can use the MCU RTC to set the external RTC data and time.

from machine import I2C, Pin, I2C, RTC
from ds3231 import DS3231
import time

DAYS = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]

i2c = I2C(1, sda=Pin.board.GP6, scl=Pin.board.GP7 )

print( "== MCU datetime ============================= ")
mcu_rtc = RTC()
_time = mcu_rtc.datetime()
#print( "mcu localtime: Year: %s, month: %s, day: %s, weekday: %s, hour: %s, min: %s, sec: %s, sub-sec:%s" % _time )
print( "mcu datetime :" , _time )
print( "mcu time     : %i secs" % time.mktime(_time) )
print( "mcu localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*_time) )
print( 'Weekday      : %s' % DAYS[_time[3]] )

print( "== DS datetime ============================== ")
print( "Set RTC time from mcu...")
rtc = DS3231( i2c )
rtc.datetime( _time ) 

print( "Read back RTC time...")
_time = rtc.datetime()
print( "RTC datetime :" , _time ) # (Y,M,D,WeekDay,H,m,S,YearDay)
print( "RTC time     : %i secs" % time.mktime(_time) )
print( "RTC localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*_time) )
weekday = _time[3]
print( 'Day of week  : %s' % DAYS[weekday] )
