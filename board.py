import sys
import machine

i2cbus = None

def init():
	global i2cbus
	if m5():
		machine.freq(240000000)
		if m5core():
			i2cbus = machine.I2C(1, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
		elif m5atom():
			# AtomS3 port A, pin G1, G2 // Using I2C bus 1, 0 is alreadu used by LP5562
			i2cbus = machine.I2C(1, scl=machine.Pin(1), sda=machine.Pin(2), freq=400000)
		else:
			i2cbus = None

def m5atom():
	return "M5Stack AtomS3" in str(sys.implementation._machine)

def m5core():
	return "Generic ESP32" in str(sys.implementation._machine)

def m5():
	return m5core() or m5atom()

def pico():
	return not m5()

def ifpico(v1, v2):
	if pico():
		return v1
	else:
		return v2

if m5():
	import esp32

def temperature():
	# CPU Temp
	if pico():
		sensor_temp = machine.ADC(4)
		reading_temp = sensor_temp.read_u16()* (3.3/65535)
		temp = 27 - (reading_temp - 0.706) / 0.001721
	elif m5core():
		temp = esp32.raw_temperature()*1.0
		temp = (temp-32)*(5/9)
	else:
		temp = esp32.mcu_temperature()*1.0
	return temp

def readi2cReg(i2c, addr, reg):
	buf = bytearray(1)
	i2c.readfrom_mem_into(addr, reg, buf)
	return int(buf[0])

def batteryLevel():
	global i2cbus

	# Battery Level
	if m5atom():
		pin = machine.Pin(8, mode=machine.Pin.IN)
		sensor_bat = machine.ADC(pin, atten=machine.ADC.ATTN_11DB)
		bat = sensor_bat.read_u16()*(4.3/65535)
		if bat < 1.0:
			bat = None
		else:
			bat = "{:.1f}".format(bat)
	elif m5core() and i2cbus is not None:
		# M5Stack Core : IP5306 power management chip at 0x75
		devices = i2cbus.scan()
		if 0x75 not in devices:
			return None

		buf = bytearray(1)
		# read registers READ0 = 0x70, READ1 = 0x71, READ3 = 0x78
		reg0 = readi2cReg(i2cbus, 0x75, 0x70)
		reg1 = readi2cReg(i2cbus, 0x75, 0x71)
		reg3 = readi2cReg(i2cbus, 0x75, 0x78)
		#print("Reg0:0x{0:02x}".format(reg0))
		#print("Reg1:0x{0:02x}".format(reg1))
		#print("Reg3:0x{0:02x}".format(reg3))
		tag = ""
		if reg0&0x08:
			# is charging
			if reg1&0x08:
				tag = "=" # charging full
			else:
				tag = "+"	# charging
		level = reg3&0xF0
		if level == 0xE0:
			bat = str(25)+tag
		elif level == 0xC0:
			bat = str(50)+tag
		elif level == 0x80:
			bat = str(75)+tag
		elif level == 0x00:
			bat = str(100)+tag
		else:
			bat = None
	else:
		bat = None
	return bat

if __name__ == "__main__":
	init()
	print("M5Stack AtomS3:", m5atom())
	print("M5Stack Core:", m5core())
	print("Pico:", pico())
	print("Temperature:", temperature())
	print("Battery Level:", batteryLevel())