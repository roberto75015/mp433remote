
import board
import time
from machine import Pin 

def buttonirq(pin):
    global _buttonLastEvent
    global _buttonLastDown
    global _buttonLastEventTicks
    global _buttonCount

    v = pin.value()
    now = time.ticks_ms()
    if v == 0:
        if time.ticks_diff(now, _buttonLastDown) > 50:
            _buttonLastDown = now
    elif v == 1:
        if time.ticks_diff(now, _buttonLastEvent) > 50:
            _buttonLastEvent = now
            _buttonLastEventTicks = time.ticks_diff(now, _buttonLastDown)
            _buttonCount += 1
    #print("Button pressed: ", v, now, _buttonLastEvent, _buttonLastDown, _buttonCount)

def count():
    global _buttonCount
    return _buttonCount

def lastEvent():
    global _buttonLastEvent
    return _buttonLastEvent

def lastEventTicks():
    global _buttonLastEventTicks
    return _buttonLastEventTicks

def init():
    global bpin
    global _buttonLastEvent
    global _buttonLastDown
    global _buttonCount
    _buttonCount = 0
    _buttonLastEvent = time.ticks_ms()
    _buttonLastDown = time.ticks_ms()
    if board.pico():
        bpin = Pin(5, mode=Pin.IN, pull=Pin.PULL_UP)
    elif board.m5atom():
        bpin = Pin(41, mode=Pin.IN)
    elif board.m5core():	# LCR: 39,38,37
        bpin = Pin(38, mode=Pin.IN)
    bpin.irq(handler=buttonirq)
