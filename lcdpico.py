from machine import I2C, Pin
from drivers.DIYables_MicroPython_LCD_I2C import LCD_I2C

# LCD setup
I2C_ADDR = 0x27
LCD_ROWS = 2
LCD_COLS = 16

def lines():
    return LCD_ROWS

def columns():
    return LCD_COLS

def init():
    global i2c, lcd_i2c
    global I2C_ADDR

    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    lcd_i2c = LCD_I2C(i2c, I2C_ADDR, LCD_ROWS, LCD_COLS)
    lcd_i2c.backlight_on()
    lcd_i2c.clear()

def print00(col, line, message):
    global lcd_i2c
    lcd_i2c.set_cursor(col, line)
    lcd_i2c.print(message)

def backlight_on():
    global lcd_i2c
    lcd_i2c.backlight_on()

def backlight_off():
    global lcd_i2c
    lcd_i2c.backlight_off()

def clear():
    global lcd_i2c
    lcd_i2c.clear()
