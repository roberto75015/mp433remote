import board

if board.m5():
    import lcdm5 as lcdll
    scrollfreq = 0
else:
    import lcdpico as lcdll
    scrollfreq = 4
    
backlight_is_on = True

def lines():
    return lcdll.lines()

def centerLine():
    return (lines()-1) // 2

def columns():
    return lcdll.columns()

def clear_linez():
    global linez, linezo, scrollcount
    linez = [""] * lines()
    linezo = [0] * lines()
    scrollcount = 0

def init():
    lcdll.init()
    clear_linez()

def printlineCenter(line, message):
    if len(message) < columns():
        nspaces = (columns()-len(message)) // 2
        message = '                    '[:nspaces]+message
    printline(line, message)

def printlineRight(line, message):
    if len(message) < columns():
        nspaces = columns()-len(message)
        message = '                    '[:nspaces]+message
    printline(line, message)

def printline(line, message):
    global linez, linezo
    linezo[line] = 0
    if linez[line] != message:
        linez[line] = message
        printline0(line, message)

def printline0(line, message):
    if len(message) < columns():
        message += '                    '[:columns()-len(message)]
    lcdll.print00(0, line, message)

def hscrolling(line):
    global linez, linezo
    return len(linez[line]) > columns() and linezo[line] != 0

def hscroll():
    global linez, linezo, scrollcount
    scrollcount += 1
    if scrollfreq != 0:
        if (scrollcount%scrollfreq) != 0:
            return
    for line in range(lines()):
        if len(linez[line]) > columns():
            if linezo[line] > 1+len(linez[line])-columns():
                linezo[line] = 0
            else:
                linezo[line] = linezo[line] + 1
            offset = linezo[line]
            printline0(line, linez[line][offset:])

def screenLines():
    global linez
    return linez

def backlightOn():
    global backlight_is_on
    lcdll.backlight_on()
    if backlight_is_on:
        linezo = [0] * lines()
    backlight_is_on = True

def backlightOff():
    global backlight_is_on
    lcdll.backlight_off()
    backlight_is_on = False

def clear():
    global linez
    lcdll.clear()
    clear_linez()

