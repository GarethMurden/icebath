# Temperature projector

A full-screen app for the Raspberry Pi that displays a logo on start-up, then a live updating temperature reading from a connected sensor. Two versions are available, one for the Raspberry Pi Zero and one for the Raspberry Pi Pico.

# Raspberry Pi Zero

## Software

Clone this repo

`git clone https://bitbucket.org/pangolinpaw/projector.git`

Install dependencies

`cd projector`

`cd zero`

`pip install -r requirements.txt --break-system-packages`

Enable temperature sensor by editing config.txt

`sudo nano /boot/firmware/config.txt`

And adding the following line to the end, substituting `x` for the required pin (the hardware section below assumes you'll be using `27`)

`dtoverlay=w1-gpio,gpiopin=27`

Save & quit by pressing `cmd` + `x` then `y`

Next create a new autostart file

`sudo nano /etc/xdg/autostart/projector.desktop`

And add the following lines

```
[Desktop Entry]
Name=Projector
Exec=/usr/bin/python3 /home/pi/projector/zero/main.py
```

Save & quit by pressing `cmd` + `x` then `y`

To remove the splash screen that shows on boot, follow https://raspberrypi.stackexchange.com/a/136786

To hide the taskbar, follow https://raspberrypi.stackexchange.com/a/143902

To hide the cursor, replace the cursor icon:

`sudo mv /usr/share/icons/PiXflat/cursors/left_ptr /usr/share/icons/PiXflat/cursors/left_ptr.bak`

Then reboot the Pi

`sudo reboot`

## Hardware

### Sensor

1. Connect the yellow data line to GPIO 27
2. Connect 3.3V (from the power pin or from pin 17)
3. Connect these two together by the resistor
4. Connect Ground

There's a [tutorioal by the Pi Hut](https://thepihut.com/blogs/raspberry-pi-tutorials/18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20), but note the different pins.


### Button

Pressing this optional button cycles through an adjutment to the temperature, 0.5 degrees per press between -10 and 10 degrees in case the sensor needs calibration.

1. Connect GPIO 14
2. Connect Ground

## Usage

```
usage: python main.py [-h] [-w]

options:
  -h, --help    show this help message and exit
  -w, --window  open in window mode, instead of full-screen
```

### Logo

To customise the logo, replace `assets/logo.png` with a new transparent background PNG image. Note that the image must have a high enough resolution for whatever screen or projector is connected to the Pi to prevent pixellation.

### Demo

![animation showing logo fade to reveal a temperature reading that updates every 4 seconds](https://bitbucket.org/pangolinpaw/projector/raw/de4a6fa7137e3ecd25a56eb3aa9c424d516fcf2d/screenshots/zero_demo.gif)


------


# Pico

## Software

Clone this repo

`git clone https://bitbucket.org/pangolinpaw/projector.git`

Install CircuitPython on the Pico

Copy the contents of the `pico` folder to the Pico

These are based on two bundles from adafruit:
- [1-wire temperature sensor](https://learn.adafruit.com/elements/2979797/download?type=zip)
- [DVI/HDMI board](https://learn.adafruit.com/elements/3145184/download?type=zip)


## Hardware

Connect the PiCowbell DVI board acording to this tutorial:

https://learn.adafruit.com/adafruit-picowbell-dvi-output

Connect the 1-wire temperature sensor according to this tutorial, but using GP0 for power and GP3 for data:

https://learn.adafruit.com/using-ds18b20-temperature-sensor-with-circuitpython/hardware

## Usage

The Pico will automatically run the application as soon as it has power, sending the output to the HDMI screen.

### Logo

To customise the logo, replace `pico/logo.bmp` with a new bitmap image of the same 320x240 dimensions.

### Demo

![video of monitor that displays a logo, then a temperature reading that updates every 10 seconds](https://bitbucket.org/pangolinpaw/projector/raw/de4a6fa7137e3ecd25a56eb3aa9c424d516fcf2d/screenshots/pico_demo.gif)

