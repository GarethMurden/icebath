import os
import glob
import platform
import time
import random

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

DEVICE = None
PREVIOUS = None

def init():
    global DEVICE
    GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH) # Provide 3.3V from pin 17
    os.system('modprobe w1-gpio')  # Turns on the 1-wire GPIO module
    os.system('modprobe w1-therm') # Turns on the Temperature module

    # Finds the correct device file that holds the temperature data
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    DEVICE = device_folder + '/w1_slave'

def read():
    try:
        if DEVICE is None:
            init()
        f = open(DEVICE, 'r') # Opens the temperature device file
        lines = f.readlines() # Returns the text
        f.close()

        # While the first line does not contain 'YES', wait for 0.2s
        # and then read the device file again.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()

        # Look for the position of the '=' in the second line of the
        # device file.
        equals_pos = lines[1].find('t=')

        # If the '=' is found, convert the rest of the line after the
        # '=' into degrees Celsius, then degrees Fahrenheit
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = round(float(temp_string) / 1000.0, 1)
            temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 1)
            return temp_c, temp_f
    except:
        return None, None

def simulate():
    '''Simulate reading from temperature sensor during development'''
    global PREVIOUS
    if PREVIOUS is None:
        result = 5.1
    else:
        values = [0]#[x/10 for x in range(0, 5)]
        if random.choice([0, 1]) == 1:
            result = round(PREVIOUS + random.choice(values), 1)
        else:
            result = round(PREVIOUS - random.choice(values), 1)
    PREVIOUS = result
    return result, result + 32

if __name__ == '__main__':
    while True:
        print(read())
        time.sleep(2)
