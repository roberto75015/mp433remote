import board

from drivers import sht4x as sht4x
from drivers import bme280 as bme280

sht40 = None
bmp280 = None

# manage to read values from SHT40 and BMP280 sensors connected on i2c bus, if detected
def sensorValues():
    global sht40, bmp280

    r1 = r2 = ""
    if board.i2cbus is not None:
        s = board.i2cbus.scan()
        if 0x44 in s:
            if sht40 is None:
                sht40 = sht4x.SHT4X(board.i2cbus)
            for x in range(2):
                try:
                    temp, rh = sht40.measurements
                    r1 = "{:.1f}C {:.1f}%".format(temp, rh)
                    break
                except Exception as e:
                    print("Error reading SHT40:", e)
        if 0x76 in s:
            # we have a BMP280, which does not provide humidity
            if bmp280 is None:
                bmp280 = bme280.BME280(i2c=board.i2cbus)
            temp2, pres, hum = bmp280.read_compensated_data()
            r2 = "{:.1f}hPa".format(pres/25600)
    if r1 == "" and r2 == "":
        return None
    if r1 != "" and r2 != "":
        return r1+" "+r2
    return r1+r2

if __name__ == "__main__":
    board.init()
    print("Sensor values:", sensorValues())