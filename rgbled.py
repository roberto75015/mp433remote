import neopixel
import machine
import board
import time

def testrgb():
    print("Running tests...")
    pwr = machine.Pin(19, mode=machine.Pin.OUT)
    rgb = neopixel.NeoPixel(machine.Pin(20), 1)
    pwr.value(1)  # Turn on power
    rgb[0] = (255, 0, 0)  # Set RGB to red
    rgb.write()  # Write to the NeoPixel
    print("Power on, RGB set to red.")
    time.sleep(5)
    rgb[0] = (0, 255, 0)
    rgb.write()  # Write to the NeoPixel
    print("Power on, RGB set to green.")
    time.sleep(5)
    rgb[0] = (0, 0, 255)
    rgb.write()  # Write to the NeoPixel
    print("Power on, RGB set to blue.")
    time.sleep(5)
    pwr.value(0)  # Turn on power
    print("Power off.")


if __name__ == "__main__":
    board.init()
    testrgb()