"""M5STACK AtomS3 128x128 (GC9107), backlight controlled by LP5562

https://docs.m5stack.com/en/core/AtomS3R

"""

from machine import Pin, SPI, I2C
import drivers.st7789py as st7789
from drivers import lp5562

TFA = 1
BFA = 3
WIDE = 1
TALL = 0
SCROLL = 0      # orientation for scroll.py
FEATHERS = 1    # orientation for feathers.py
blctl = None

def config(rotation=0):
    """
    Configures and returns an instance of the ST7789 display driver.

    Args:
        rotation (int): The rotation of the display (default: 0).

    Returns:
        ST7789: An instance of the ST7789 display driver.
    """
    global blctl

    blctl = lp5562.LP5562()
    blctl.begin()
    backlight_on()

    return st7789.ST7789(
        SPI(2, baudrate=40000000, sck=Pin(15), mosi=Pin(21), miso=None),
        128,
        128,
        reset=Pin(48, Pin.OUT),
        cs=Pin(14, Pin.OUT),
        dc=Pin(42, Pin.OUT),
        backlight=None,
        rotation=rotation,
        color_order=st7789.BGR,
    )

def backlight_set(value):
    global blctl
    if blctl is not None:
        blctl.set_brightness(0, value)
        blctl.set_brightness(1, value)
        blctl.set_brightness(2, value)
        blctl.set_brightness(3, value)

def backlight_on():
    backlight_set(127)

def backlight_off():
    backlight_set(0)