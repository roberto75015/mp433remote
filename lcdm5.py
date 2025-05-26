
import board
import drivers.st7789py as st7789

if board.m5atom():
    import tft_config_atoms3r as tft_config
    import fonts.vga2_8x16 as font
    bgcolor = st7789.BLACK
    fgcolor = st7789.WHITE
else:
    import tft_config_m5 as tft_config
    import fonts.vga2_16x32 as font
    fgcolor = st7789.BLACK
    bgcolor = st7789.WHITE

def lines():
    global tft
    return int(tft.height/font.HEIGHT)

def columns():
    global tft
    return int(tft.width/font.WIDTH)

def init():
    global tft, bgcolor
    tft = tft_config.config()
    tft.vscrdef(tft_config.TFA, 240, tft_config.BFA)
    tft.fill(bgcolor)

def print00(col, line, text):
    global tft, fgcolor, bgcolor
    tft.text(font, text, col*font.WIDTH, line*font.HEIGHT, fgcolor, bgcolor)

def backlight_on():
    tft_config.backlight_on()

def backlight_off():
    tft_config.backlight_off()

def clear():
    global tft
    tft.fill(bgcolor)
