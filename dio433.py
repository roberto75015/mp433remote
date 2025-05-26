
# implements remote control for a 433 MHz device using a microcontroller

import time
import board
from machine import Pin

# pin = Pin(4, Pin.OUT)
bit2 = [False] * 26  # 26 bit Identifiant emetteur
bit2Interruptor = [False] * 4

def send_bit(b):
    if b:
        pin.on()
        time.sleep_us(310)  # 310 microseconds
        pin.off()
        time.sleep_us(1340)  # 1340 microseconds
    else:
        pin.on()
        time.sleep_us(310)  # 310 microseconds
        pin.off()
        time.sleep_us(310)  # 310 microseconds

def power2(power):
    return 1 << power  # Equivalent to 2 ** power

def itob(integer, length):
    for i in range(length):
        if (integer // power2(length - 1 - i)) == 1:
            integer -= power2(length - 1 - i)
            bit2[i] = True
        else:
            bit2[i] = False

def itob_interruptor(integer, length):
    for i in range(length):
        if (integer // power2(length - 1 - i)) == 1:
            integer -= power2(length - 1 - i)
            bit2Interruptor[i] = True
        else:
            bit2Interruptor[i] = False

def send_pair(b):
    if b:
        send_bit(True)
        send_bit(False)
    else:
        send_bit(False)
        send_bit(True)

def transmit(onoff):
    pin.on()
    time.sleep_us(275)  # 275 microseconds
    pin.off()
    time.sleep_us(9900)  # 9900 microseconds
    pin.on()
    time.sleep_us(275)  # 275 microseconds
    pin.off()
    time.sleep_us(2675)  # 2675 microseconds
    pin.on()

    for i in range(26):
        send_pair(bit2[i])

    send_pair(False)  # 26th bit
    send_pair(onoff)  # 27th bit

    for i in range(4):
        send_pair(bit2Interruptor[i])

    pin.on()  # coupure données, verrou
    time.sleep_us(275)  # attendre 275µs pin.off()  # verrou 2 de 2675µs pour signaler la fermeture du signal

def dio433(onoff=False, pinno=None, sender=29014766, interruptor=0):
    global pin

    if pinno == None:
        pinno = board.ifpico(2, 5)
    pin = Pin(pinno, Pin.OUT)
    pin.off()

    itob(sender, 26)  # conversion du code de l'emetteur
    itob_interruptor(interruptor, 4)
    
    NRETRY = 10
    for _ in range(NRETRY):
         transmit(onoff)
         time.sleep_ms(10)
    time.sleep_ms(32)
