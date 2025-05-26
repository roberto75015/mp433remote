#
#  Play a note on a buzzer
#

from machine import Pin, PWM
import time
import board

def init():
    global buzzer
    if board.m5atom():
        return
    buzzer = PWM(Pin(board.ifpico(28, 25), Pin.OUT))

def playNote(frequency, duration, pause) :
    global buzzer
    if board.m5atom():
        return
    buzzer.duty_u16(board.ifpico(5000, 100))  # adjust loudness: smaller number is quieter.
    buzzer.freq(frequency)
    time.sleep(duration)
    buzzer.duty_u16(0) # loudness set to 0 = sound off
    time.sleep(pause)
    
def play(sound=0):
    if board.m5atom():
        return
    notes = [
                [440],
                [523],
                [659],
                [784],
                [440, 523],
                [659, 784],
                [440, 523, 659, 784],
                [440, 494, 523, 587, 659, 698, 784],
             ]
    
    for note in notes[sound]:
        playNote(note, 0.1, 0.01)

if __name__ == "__main__":
    init()
    play(0)  # Play the first sound
    time.sleep(1)  # Wait for a second to hear the sound
    play(1)  # Play the second sound
    time.sleep(1)  # Wait for a second to hear the sound