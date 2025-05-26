This micropython program is made to control DI-O power sockets, made from brand Cachon, using a basic 433Mhz emitter connected to a GPIO pin to emulate the remote control.
Possibly the protocol is compatible with other power sockets controlled by 433Mhz messages, to be verified on a case by case basis.

I was inspired and took the implementation of the protocol, converting to micropython, from this article: https://arno0x0x.wordpress.com/2015/04/02/rf433-outlet/, thanks to Arno0x0x

A minimal web server is also implemented, providing a web page from which the switches can be operated and the ability to control the switches via HTTP. Make sure you check SSID and password in the wifi.py file.

It runs 3 different devices:

    Raspberry Pico 2W,
    M5Stack AtomS3R,
    M5Stack Core 4M

On the Pico, I connected an 2x16 LCD display driven thru an i2c lcd controller, a buzzer for sound and a button all three connected via standard GPIO pins. The button is to scroll across the content shown on the LCD.

On the M5 stack devices the native LCD and buttons are used.

As for those M5 stack devices, I used generic appropriate ESP32 implementation of  micropython over the uiflow-micropython provided by M5, mainly to avoid the 'out of memory' error on the 4Mb M5Stack core.