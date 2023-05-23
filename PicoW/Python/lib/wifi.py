import time
import network
import machine
import ubinascii

class WIFI:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.led = machine.Pin("LED", machine.Pin.OUT)


    def scanNetworks(self):
        self.wlan = network.WLAN(network.STA_IF) 
        self.wlan.active(True) 

        print('Bezig met scannen van beschikbare draadloze netwerken...')
        accessPoints = self.wlan.scan()
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


    def getIpAddress(self):
        status = self.wlan.ifconfig()
        ipaddress = status[0]
        return ipaddress
    

    def getInfo(self):
        print('\n--------------------------------------------------------------------------------')
        print('WiFi name      : ' + self.wlan.config('ssid'))
        print('IP address     : ' + self.wlan.ifconfig()[0])
        print('Host name      : ' + self.wlan.config('hostname'))
        print('MAC address    : ' + ubinascii.hexlify(self.wlan.config('mac'),':').decode())
        print('Channel        : ' + str(self.wlan.config('channel')))
        print('Security type  : ' + str(self.wlan.config('security')))
        print('Transmit power : ' + str(self.wlan.config('txpower')))
        print('--------------------------------------------------------------------------------')


    def connect(self, ssid, password):
        if self.wlan.isconnected():
            ssid = self.wlan.config('ssid')
            print('Reeds verbonden met Wi-Fi netwerk', ssid)
        else:
            self.wlan.active(True)
            self.wlan.connect(ssid, password)

            max_wait = 10
            while max_wait > 0:
                if self.wlan.status() < 0 or self.wlan.status() >= 3:
                    break

                self.led.on()
                max_wait -= 1
                print('Wachten op connectie...')
                time.sleep(1/2)
                self.led.off()
                time.sleep(1/2)

            if self.wlan.status() != 3:
                raise RuntimeError('Verbinden met Wifi mislukt.')
                self.led.off()
            else:
                self.led.on()
                status = self.wlan.ifconfig()
                print('\nVerbonden met Wi-Fi netwerk')
                self.getInfo()
        

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect() 
            self.wlan.active(False)
            print('Verbinding met Wi-Fi netwerk verbroken.')
        else:
            print('Geen actieve verbinding met een Wi-Fi network.')

        self.led.off()



