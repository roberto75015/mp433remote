# TI LP5562

import time
from machine import I2C, Pin

class LP5562:
    LP5562_I2C_ADDRESS = 0x30
    LP5562_MAX_LEDS = 4

    # Register and constant definitions
    LP5562_REG_ENABLE = 0x00
    LP5562_MASTER_ENABLE = 0x40
    LP5562_LOGARITHMIC_PWM = 0x80
    LP5562_EXEC_RUN = 0x2A
    LP5562_ENABLE_DEFAULT = LP5562_MASTER_ENABLE | LP5562_LOGARITHMIC_PWM
    LP5562_ENABLE_RUN_PROGRAM = LP5562_ENABLE_DEFAULT | LP5562_EXEC_RUN

    LP5562_REG_OP_MODE = 0x01

    LP5562_REG_R_PWM = 0x04
    LP5562_REG_G_PWM = 0x03
    LP5562_REG_B_PWM = 0x02
    LP5562_REG_W_PWM = 0x0E

    LP5562_REG_R_CURRENT = 0x07
    LP5562_REG_G_CURRENT = 0x06
    LP5562_REG_B_CURRENT = 0x05
    LP5562_REG_W_CURRENT = 0x0F

    LP5562_REG_CONFIG = 0x08
    LP5562_CLK_INT = 0x01

    LP5562_REG_RESET = 0x0D
    LP5562_RESET = 0xFF

    LP5562_REG_ENG_SEL = 0x70

    #def __init__(self):

    def begin(self):
        self.addr = self.LP5562_I2C_ADDRESS
        self.i2c = I2C(scl=Pin(0), sda=Pin(45), freq=400000)
        self.i2c.scan()

        self._delay(1)
        self._write_register(self.LP5562_REG_ENABLE, self.LP5562_MASTER_ENABLE)
        self._delay(1)

        self._write_register(self.LP5562_REG_CONFIG, self.LP5562_CLK_INT)
        self._write_register(self.LP5562_REG_ENG_SEL, 0x00)

        # PWM clock frequency 558 Hz
        data = self._read_register(self.LP5562_REG_CONFIG)
        data      = data | 0B01000000
        # data = data & 0B10111111
        self._write_register(self.LP5562_REG_CONFIG, data)
        
        return True

    def set_led_current(self, channel, current):
        addr = [
            self.LP5562_REG_R_CURRENT,
            self.LP5562_REG_G_CURRENT,
            self.LP5562_REG_B_CURRENT,
            self.LP5562_REG_W_CURRENT,
        ]
        if channel < self.LP5562_MAX_LEDS:
            self._write_register(addr[channel], current)

    def set_brightness(self, channel, brightness):
        addr = [
            self.LP5562_REG_R_PWM,
            self.LP5562_REG_G_PWM,
            self.LP5562_REG_B_PWM,
            self.LP5562_REG_W_PWM,
        ]
        if channel < self.LP5562_MAX_LEDS:
            self._write_register(addr[channel], brightness)

    def reset(self):
        self._write_register(self.LP5562_REG_RESET, self.LP5562_RESET)

    def enable(self):
        self._write_register(self.LP5562_REG_ENABLE, self.LP5562_ENABLE_DEFAULT)

    def disable(self):
        self._write_register(self.LP5562_REG_ENABLE, 0x00)

    def run_program(self):
        self._write_register(self.LP5562_REG_ENABLE, self.LP5562_ENABLE_RUN_PROGRAM)

    def stop_program(self):
        self._write_register(self.LP5562_REG_ENABLE, self.LP5562_ENABLE_DEFAULT)

    def _write_register(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    def _read_register(self, reg):
        return int.from_bytes(self.i2c.readfrom_mem(self.addr, reg, 1), 'little')

    def _delay(self, ms):
        time.sleep_ms(ms)

