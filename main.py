
import sys
import time
import asyncio

import board
import switches
import button
import buzzer
import timesync
import lcd
import wifi
import env4sensor
import webserver

def getScreenContent(page, pageSize):
    lines = []
    firstLine = pageSize*page
    for i in range(pageSize):
        x = (i+firstLine)%6
        s = 0
        if x == s:
            t = ""
            for i in range(switches.nswitches()):
                t += " " if t != "" else ""
                interruptor = switches.switches[i]
                #t += f"{interruptor[0]}:"
                t += f"S{i}:"
                t += "1" if switches.state[i] else "0"
            lines.append(t)
        elif x == (s:=s+1):
            # signal level
            signal = wifi.wlan.status('rssi')
            ifconfig = wifi.wlan.ifconfig()
            lines.append("wifi:"+wifi.ssid+" IP:"+ifconfig[0]+" "+str(signal))
        elif x == (s:=s+1):
            t = env4sensor.sensorValues()
            if t is not None:
                t = t + str.format(" {:.1f}C", board.temperature())
            else:
                t = str.format("CPU Temp: {:.1f}C", board.temperature())
            lines.append(t)
        elif x == (s:=s+1):
            # battery level
            level = board.batteryLevel()
            if level is not None:
                lines.append("Battery: "+str(level))
            else:
                lines.append("No battery")
        elif x == (s:=s+1):
            t = '.'.join(str(x) for x in sys.implementation.version if x != '')
            lines.append("Micropython "+t)
        elif x == (s:=s+1):
            t = str(sys.implementation._machine)
            #t = t.replace("Raspberry Pi ", "")
            t = t.replace("with ", "")
            lines.append(t)
    return lines

async def main():
    wifi.connect()

    lcd.printlineCenter(lcd.centerLine(), "Syncing time..")
    timesync.sync(local="xwaregw" in wifi.ssid)
    lcd.printline(lcd.centerLine(), "")

    asyncio.create_task(asyncio.start_server(webserver.webserver, "0.0.0.0", 80))

    if board.pico():
        LOOP_SLEEP = 250
    else:
        LOOP_SLEEP = 1000
    LCD_TIMER = 60

    lastLastEvent = button.lastEvent()
    lcdOnTimer = time.time()+LCD_TIMER
    prevNrequests = webserver.nrequests
    prevtime = time.localtime()
    prevTickMs = time.ticks_ms()
    page = 0
    sleepMs = 0

    while True:
        lastEvent = button.lastEvent()
        if lastEvent != lastLastEvent:
            lastLastEvent = lastEvent
            buttonPressed = True
        else:
            buttonPressed = False

        if prevNrequests != webserver.nrequests:
            prevNrequests = webserver.nrequests
            if lcdOnTimer == 0:
                lcdOnTimer = time.time()+LCD_TIMER
                page = 0
                lcd.backlightOn()

        if buttonPressed:
            if lcdOnTimer == 0:
                lcd.backlightOn()
            else:
                page += 1
            lcdOnTimer = time.time()+LCD_TIMER
        elif lcdOnTimer > 0:
            if time.time() > lcdOnTimer:
                lcdOnTimer = 0
                lcd.backlightOff()

        if lcdOnTimer != 0:
            lines = getScreenContent(page, lcd.lines()-1)
            for lineno in range(lcd.lines()-1):
                if lines[lineno] != None:
                    if buttonPressed or not lcd.hscrolling(lineno):
                        lcd.printline(lineno, lines[lineno])

            t = time.localtime()
            for x in range(3, 6):
                if t[x] != prevtime[x]:
                    sleepMsDebug = ""
                    #sleepMsDebug = str(sleepMs)+"< "
                    lcd.printlineRight(lcd.lines()-1, sleepMsDebug + str.format("{:02d}:{:02d}:{:02d}", t[3], t[4], t[5]))
                    break
            prevtime = t
            if buttonPressed:
                buzzer.play(page%4)

        sleepMs = LOOP_SLEEP - time.ticks_diff(time.ticks_ms(), prevTickMs)
        await asyncio.sleep_ms(max(0, sleepMs))
        prevTickMs = time.ticks_ms()

        if lcdOnTimer != 0:
            lcd.hscroll()


# Initialize everything
board.init()
lcd.init()
button.init()
buzzer.init()
buzzer.play(7)

# Main loop to listen for connections
while True:
    try:
        asyncio.run(main())       
    except KeyboardInterrupt:
        lcd.clear()
        lcd.backlightOn()
        lcd.printlineCenter(lcd.centerLine(), "stopped")
        time.sleep(2)
        lcd.backlightOff()
        raise
    finally:
        asyncio.new_event_loop()
