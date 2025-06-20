import time
import board
import digitalio
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Use GPIO 0 to supply 3.3V
sensor_voltage = digitalio.DigitalInOut(board.GP0)
sensor_voltage.direction = digitalio.Direction.OUTPUT
sensor_voltage.value = True

# Initialise 1-wire sensor
ow_bus = OneWireBus(board.GP3)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

def current():
    return '{0:0.1f}c'.format(ds18.temperature)

