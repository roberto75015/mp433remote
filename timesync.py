import socket
import json
import machine
import time

def last_sunday(year, month):
    """Ritorna la data dell'ultima domenica di un dato mese."""
    # Parti dal giorno 31 e vai a ritroso
    for day in range(31, 24, -1):  # Ultima settimana del mese
        try:
            t = time.mktime((year, month, day, 0, 0, 0, 0, 0))
            weekday = time.localtime(t)[6]  # 6 = domenica
            if weekday == 6:
                return (year, month, day)
        except:
            continue
    return None

def is_dst_europe():
    """Verifica se l'ora legale è attiva in Europa (approssimato, valido per CET/CEST)."""
    now = time.localtime()
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[3]

    # Ultima domenica di marzo alle 2:00
    start = last_sunday(year, 3)
    # Ultima domenica di ottobre alle 3:00
    end = last_sunday(year, 10)

    if start is None or end is None:
        return False  # Non può calcolare

    # Confronta date
    if (month > 3 and month < 10):
        return True
    elif month == 3:
        if day > start[2]:
            return True
        elif day == start[2] and hour >= 2:
            return True
    elif month == 10:
        if day < end[2]:
            return True
        elif day == end[2] and hour < 3:
            return True

    return False

def xwsettime():
    addr = socket.getaddrinfo("192.168.1.1", 880)[0][-1]
    s = socket.socket()
    try:
        s.settimeout(12)
        s.connect(addr)
        s.settimeout(4)
        s.send("GET /localtime.php\r\n\r\n")
        msg = s.recv(512)
    except Exception as err:
        msg = None
    finally:
        s.close()
    if msg != None:
        t = json.loads(msg)
        machine.RTC().datetime((t['tm_year']+1900, t['tm_mon']+1, t['tm_mday'], 0, t['tm_hour'], t['tm_min'], t['tm_sec'], 0))

def sync(local=False):
    if local:
        xwsettime()
    else:
        import ntptime
        ntptime.timeout=8
        try:
            t = ntptime.time()
        except Exception as err:
            print("NTP error:", err)
            return
        t += 3600
        if is_dst_europe():
            t += 3600
        tm = time.gmtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

if __name__ == "__main__":
    xwsettime()
    if is_dst_europe():
        print("Ora legale attiva in Europa.")
    else:
        print("Ora solare attiva in Europa.")