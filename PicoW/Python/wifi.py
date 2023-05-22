import time
import network
import machine

class WIFI:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.led = machine.Pin("LED", machine.Pin.OUT)
    #end def


    def getIpAddress(self):
        status = self.wlan.ifconfig()
        ipaddress = status[0]
        return ipaddress
    #end def


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
                #endif
                self.led.on()
                max_wait -= 1
                print('Wachten op connectie...')
                time.sleep(1/2)
                self.led.off()
                time.sleep(1/2)
            #endloop

            if self.wlan.status() != 3:
                raise RuntimeError('Verbinden met Wifi mislukt.')
                self.led.off()
            else:
                self.led.on()
                status = self.wlan.ifconfig()
                print('Verbonden met Wi-Fi netwerk %s. IP adres: %s' % (ssid, status[0]) )
            #endif
        #endif
    #end def    
        

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect() 
            self.wlan.active(False)
            print('Verbinding met Wi-Fi netwerk verbroken.')
        else:
            print('Geen actieve verbinding met een Wi-Fi network.')
        #endif
        self.led.off()
    #end def

#endclass
