
from machine import UART
from machine import Timer
import time
import sys

class atgm336h():
    def __init__(self, id: Literal[0, 1, 2], tx: int, rx: int):
        self.mode = 0
        self.antenna_state = "0"
        self.gps_time = ["00", "00", "00"]
        self.gps_date = ["00", "00", "00"]
        self.gps_date_time = ["00", "00", "00", "00", "00", "00"]
        self.timestamp = 0
        self.latitude = "0N"
        self.longitude = "0E"
        self.altitude = "0"
        self.satellite_num = "0"
        self.pos_quality = "0"
        self.corse_ground_degree = "0"
        self.speed_ground_knot = "0"
        self.time_offset = 0
        self.uart = UART(id, tx=tx, rx=rx)
        self.uart.init(115200, bits=8, parity=None, stop=1, rxbuf=1024)
        self._timer = Timer(0)
        self._timer.init(mode=Timer.PERIODIC, freq=1, callback=self._monitor)
        self.set_work_mode(7)
        buf = self._add_checksum(f"PCAS02,1000")    # Set update rate to 1 second
        self.uart.write(buf.encode())
        self.last_active = 0

    def __del__(self):
        self.deinit()

    def is_active(self):
        return time.time() - self.last_active < 5

    def set_work_mode(self, mode: int):
        self.mode = mode
        buf = self._add_checksum(f"PCAS04,{mode}")
        self.uart.write(buf.encode())

    def get_work_mode(self):
        return self.mode

    def get_antenna_state(self) -> str:
        return self.antenna_state

    def get_gps_time(self):
        return self.gps_time

    def get_gps_date(self):
        return self.gps_date

    def get_gps_date_time(self):
        return self.gps_date_time

    def get_timestamp(self) -> int | float:
        return self.timestamp

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_altitude(self):
        return self.altitude

    def get_satellite_num(self):
        return self.satellite_num

    def get_pos_quality(self):
        return self.pos_quality

    def get_corse_over_ground(self) -> str:
        return self.corse_ground_degree

    def get_speed_over_ground(self) -> str:
        return self.speed_ground_knot

    def set_time_zone(self, value):
        self.time_offset = value

    def get_time_zone(self):
        return self.time_offset

    def deinit(self):
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass

    def _add_checksum(self, message: str) -> str:
        checksum = 0
        for char in message:
            checksum ^= ord(char)
        return f"${message}*{checksum:02X}\r\n"

    def _decode_gga(self, data: str):
        gps_list = data.split(",")
        self.pos_quality = gps_list[6]
        if self.pos_quality == "0":
            return
        self.satellite_num = gps_list[7]
        if gps_list[9]:
            self.altitude = gps_list[9] + gps_list[10]

    def _decode_rmc(self, data: str):
        gps_list = data.split(",")
        if gps_list[2] == "A":
            time_buf = gps_list[1]
            self.gps_time = [
                int(time_buf[0:2]) + self.time_offset,
                int(time_buf[2:4]),
                int(time_buf[4:6]),
            ]
            self.latitude = self._convert_to_decimal(gps_list[3], gps_list[4])
            self.longitude = self._convert_to_decimal(gps_list[5], gps_list[6], False)
            self.speed_ground_knot = gps_list[7]
            self.corse_ground_degree = gps_list[8]
            data_buf = gps_list[9]
            self.gps_date = [int(data_buf[4:7]) + 2000, int(data_buf[2:4]), int(data_buf[0:2])]
            t = (
                self.gps_date[0],
                self.gps_date[1],
                self.gps_date[2],
                self.gps_time[0] - self.time_offset,
                self.gps_time[1],
                self.gps_time[2],
                0,
                0,
            )
            self.gps_date_time = self.gps_date + self.gps_time
            buf = time.mktime(t)
            self.timestamp = buf

    def _convert_to_decimal(self, degrees_minutes, direction, latitude: bool = True) -> float:
        if latitude:
            degrees = degrees_minutes[:2]  # First two digits are degrees
            minutes = degrees_minutes[2:]  # The rest are minutes
        else:
            degrees = degrees_minutes[:3]
            minutes = degrees_minutes[3:]
        decimal = int(degrees) + round(float(minutes) / 60.0, 6)
        if direction in ["S", "W"]:
            decimal = -decimal
        return decimal

    def _decode_txt(self, data: str):
        gps_list = data.split(",")
        if gps_list[4] is not None and gps_list[4][0:7] == "ANTENNA":
            self.antenna_state = gps_list[4][8:].split("*")[0]

    def _monitor(self, t):
        while True:
            if self.uart.any() < 25:
                break
            gps_data = self.uart.readline()
            if gps_data is not None and isinstance(gps_data, bytes):
                self.last_active = time.time()
                if gps_data[3:6] == b"GGA" and gps_data[-1] == b"\n"[0]:
                    self._decode_gga(gps_data.decode())
                elif gps_data[3:6] == b"RMC" and gps_data[-1] == b"\n"[0]:
                    self._decode_rmc(gps_data.decode())
                elif gps_data[3:6] == b"TXT" and gps_data[-1] == b"\n"[0]:
                    self._decode_txt(gps_data.decode())
