
import board
import drivers.atgm336h as atgm336h

if board.m5():
    gps = atgm336h.atgm336h(1, tx=2, rx=1)
else:
    gps = None

def active():
    return gps is not None and gps.is_active() 

def data():
    if not active():
        return None
    return "GPS : {}, {}, {}, {}, {}, {}".format(
        gps.get_latitude(),
        gps.get_longitude(),
        gps.get_altitude(),
        gps.get_speed_over_ground(),
        gps.get_satellite_num(),
        gps.get_pos_quality()
    )