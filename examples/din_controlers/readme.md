# DinControler class test

DinControler and descendant classes are used to ease access to the hardware (and behaviour it can offers).

The DinControner class can be used with :

* __Synchronous call__ : scripts start with "sync" names.
* __Asynchronous call__ : scripts starts with "async" name.

## Synchronous usage

Regular Python script run their content in a synchronous matter. Each function call must be completely executed before returning the code execution to the callee. 

It is the most simple way to create and run your script.
Script mist take case of error management and continuous code execution.

Synchronous examples starts with __sync___ name.

## Asynchronous usage

Based on AsyncIO (also available under MicroPython), if allows the script to run tasks in a concurrent matter. 

The DinControler class also offers various facilities the user code in a AsyncIO environment.

Asynchronous examples starts with __async___ filename.

## Useful asyncio ressources
* [asyncio - Asynchronous I/O](https://docs.python.org/3/library/asyncio.html) Python 3
* [asyncio - Event Loop](https://docs.python.org/3/library/asyncio-eventloop.html) Python 3
* [asynio - Running & stopping the loop](https://docs.python.org/3/library/asyncio-eventloop.html#running-and-stopping-the-loop) Python 3

# Examples

Small word about examples.

## Common 

* [async-exception.py](common/async-exception.py) : exception in ''userloop'' terminate the code excution. Raised exception can still be checked after ends of execution.
* [async-scheduler.py](common/async-scheduler.py) : using an asynchronous scheduler to execute date & time scheduled tasks. Create a myDin Task to run the scheduler.
* [common/async-watchdog.py](common/async-watchdog.py) : activate the watchdog and test its effectiveness by helding the button 1 for more than 2 seconds (blocks the ''userloop'')

## Pico3Mod 

* [async-read-buttons.py](pico3mod/async-read-buttons.py) : Just check buttons and toggle the LED state.
* [async-read-ds18b20.py](pico3mod/async-read-ds18b20.py) : Just read DS18B20 temperature (as acquired by the ds18b20 asynchronous tasks)
* [async-read-bme280.py](pico3mod/async-read-bme280.py) : Connect a BME280/BMP280 atmospheric pressure sensor on the I2C bus (Qwiic connector) and reads it data every 10 seconds (in the ''userloop'', non blocking approach)
* [async-read-serlcd.py](pico3mod/async-read-serlcd.py) : Connect a SparkFun SerLCD on the I2C bus (Qwiic connector) and display internal temperature every 5 seconds (in the ''userloop'', non blocking way)

Procedural examples:
* [sync-read-buttons.py](pico3mod/sync-read-buttons.py) : Check if a button was pressed (and toggle the LED state)
* [sync-read-ds18b20.py](pico3mod/sync-read-ds18b20.py) : blocking read of the DS18B20 temperature