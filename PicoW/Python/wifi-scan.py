import network
import machine
import ubinascii

def main():
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True) 

    print('Bezig met scannen van beschikbare draadloze netwerken...')
    accessPoints = wlan.scan()
    print('Gereed.')

    authmodes = ['Open', 'WEP', 'WPA-PSK', 'WPA2-PSK4', 'WPA/WPA2-PSK']

    print('  |SSID           |BSSID (MAC)       |Ch |Signal |Security       ')
    print('--+---------------+------------------+---+-------+---------------')

    i=0
    for (ssid, bssid, channel, rssi, authmode, hidden) in accessPoints:
        i+=1
        ssid = ssid.decode()
        bssid = ubinascii.hexlify(bssid,':').decode()
        authmode = authmodes[int(authmode)-1]
        print(f"{i:<2}|{ssid:<15}|{bssid:<18}|{channel:<3}|{rssi:<7}|{authmode:<15}")


main()