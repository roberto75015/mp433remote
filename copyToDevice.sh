#!/bin/bash
device=`mpremote exec "import sys
print(sys.implementation._machine)
"`



# copy common files
echo "*** Copying Common files"
mpremote cp board.py button.py buzzer.py dio433.py env4sensor.py lcd.py main.py switches.py timesync.py webserver.py wifi.py wifiConfig.py :
mpremote mkdir drivers
mpremote cp drivers/bme280.py drivers/sht4x.py :drivers/


case $device in
*RP2040*)
	echo "*** Copying RPY Pico files"
	mpremote cp lcdpico.py :
	mpremote cp drivers/DIYables_MicroPython_LCD_I2C.py :drivers/
	;;
*AtomS3*)
	echo "*** Copying Atom files"
	mpremote cp tft_config_atoms3r.py :
	mpremote cp drivers/lp5562.py :
	;;
*ESP32*)
	echo "*** Copying M5Core files"
	mpremote cp tft_config_m5.py :
	;;
esac

case $device in
*AtomS3*|*ESP32*)
	echo "*** Copying M5Stack common files"
	mpremote mkdir fonts
	mpremote cp fonts/*.mpy :fonts/
	mpremote cp lcdm5.py :
	mpremote cp drivers/st7789py.py :drivers/
	;;
esac
