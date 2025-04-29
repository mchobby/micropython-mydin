""" dincase-mb3pico - read external DS3132 RTC to set MCU RTC datetime """

from machine import I2C, Pin, I2C, RTC
from ds3231 import DS3231
import time

DAYS = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]

i2c = I2C(1, sda=Pin.board.GP6, scl=Pin.board.GP7 )

print( "== Initial MCU datetime ===================== ")
mcu_rtc = RTC()
_time = mcu_rtc.datetime()
print( "mcu datetime :", _time )
print( "mcu time     : %s secs" % time.mktime(_time) )
print( "mcu localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*_time) )
print( 'Weekday      : %s' % DAYS[_time[3]] )

print( "== DS datetime ============================== ")
ds_rtc = DS3231( i2c )
_time = ds_rtc.datetime()
print( "RTC datetime :", _time ) # ( Y,M,D,WeekDay,H,m,S,YearDay)
print( "RTC time     : %s secs" % time.mktime(_time) )
print( "RTC localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*_time) )
weekday = _time[3]
print( 'Day of week  : %s' % DAYS[weekday] )

print( "== MCU datetime ============================= ")
print( "set MCU time from PCF RTC...")
#ltime = time.localtime(pcf_rtc.datetime)

mcu_rtc = RTC()
# yearn month, day, day_of_week, hour, min, sec, day_of_year-or-zero
mcu_rtc.datetime( _time )
_time2 = mcu_rtc.datetime()
print( "mcu datetime :", _time2 )
print( "mcu time     : %s secs" % time.mktime(_time2) )
print( "mcu localtime: {2}/{1}/{0} {4}:{5}:{6}".format(*_time2) )
print( 'Weekday      : %s' % DAYS[_time2[3]] )
