
import sys
import asyncio

import switches
import lcd

nrequests = 0

# HTML template for the webpage
def webpage():
    version = '.'.join(str(x) for x in sys.implementation.version if x != '')
    linez = "\r\n".join(lcd.screenLines())
    style = "<style> pre {color: white; background-color: black;} </style>"
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            {style}
            <title>AtomS3R Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>{sys.implementation.name} {version} {sys.implementation._machine}</h1>
        """
    html += f"""
            <h2>Switches</h2>
        """
    for i in range(switches.nswitches()):
        interruptor = switches.switches[i]
        html += f"""
            <table cellspacing=0 cellpadding=0 border=0 width="50%"><tr>
                <td width="33%">Switch {i} {interruptor[0]}: {switches.state[i]}<td>
                <td width="33%"><form action="./l{i}on">
                    <input type="submit" value="l{i}on" />
                </form></td>
                <td width="33%"><form action="./l{i}off">
                    <input type="submit" value="l{i}off" />
                </form></td>
        """
    html += f"""
            <table cellspacing=0 cellpadding=0 border=0 width="50%"><tr><td>
            <code><pre>{linez}</pre></code>
            </td><tr></table>
        </body>
        </html>
        """
    return str(html)

async def webserver(reader, writer):
    global nrequests

    # Receive and parse the request
    request_line = await reader.readline()
    while await reader.readline() != b"\r\n":
        pass
    request = str(request_line)

    try:
        request = request.split()[1]
    except IndexError:
        pass

    print(f"Request received: {request}") 
    if request.startswith('/l'):
        intno = int(request[2])
        print(f"Request for switch {intno}: {request}")
        if intno >= 0 and intno < switches.nswitches():
            if request[3] == 'o' and request[4] == 'n':
                switches.switch(True, intno)
            elif request[3] == 'o' and request[4] == 'f':
                switches.switch(False, intno)

    nrequests = nrequests+1

    # Generate HTML response
    response = webpage()  

    # Send the HTTP response and close the connection
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()