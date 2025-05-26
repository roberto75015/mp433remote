import network
import time
import lcd

def connect():
    global wlan, ssid

    try:
        import wifiConfig
        wifiPass = wifiConfig.wifiPass
    except ImportError:
        wifiPass = [ ('ssid', 'pazzword'), ]
    cline = lcd.centerLine()
    lcd.printlineCenter(cline, "wifi: scannning")
    while True:
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wifiNets = wlan.scan()
            for wifiNet in wifiNets:
                ssid = wifiNet[0].decode('utf-8')
                password = None
                for cred in wifiPass:
                    if ssid == cred[0]:
                        password = cred[1]
                        break
                if password is not None:
                    lcd.printlineCenter(cline, "wifi: "+ssid)
                    wlan.connect(ssid, password)
                    break
        except Exception as e:
            print("WIFI setup error: "+str(e))
            time.sleep(1)
            continue
        connection_timeout = 10
        while connection_timeout > 0:
            status = wlan.status()
            if status == network.STAT_GOT_IP:
                lcd.clear()
                return
            if status == network.STAT_CONNECTING:
                msg = "wifi: "+ssid+" .........."[:10-connection_timeout]
            elif status < network.STAT_NO_AP_FOUND:
                msg = "wifi: access point?"
            elif status < network.STAT_WRONG_PASSWORD:
                msg = "wifi: password?"
            else:
                msg = 'searching: '+".........."[:10-connection_timeout]
            lcd.printlineCenter(cline, msg)
            connection_timeout -= 1
            time.sleep(1)