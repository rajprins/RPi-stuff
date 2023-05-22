from lcd1602 import LCD1602
from time import sleep
import network
import sys
import socket
from machine import Pin, I2C, PWM


html = """<!DOCTYPE html>
<html>
<head><title>Raspberry Pico W</title></head>
<body>
    <div style="background-color: crimson;">
        <img src="https://assets.raspberrypi.com/static/wordmark-719b92092d172dc498f9ed816f47a942.svg" height="50" />
    </div>
    <div style="background-color: silver;  height: 10px;">
        <nbsp/>
    </div>
    <p>%s</p>
</body>
</html>
"""


i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
buzzer = PWM(Pin(27)) # Aansluiten op A1
wlan = network.WLAN(network.STA_IF)
display = LCD1602(i2c, 2, 16) # Grove 16x2 LCD panel, aansluiten op I2C1


def getIpAddress():
    status = wlan.ifconfig()
    return status[0]
#end def


def connect(ssid, password):
    led = Pin("LED", Pin.OUT)
    
    # Controleer of we al verbonden zijn met een wifi netwerk
    if wlan.isconnected():
        ssid = wlan.config('ssid')
        ipaddress = wlan.ifconfig()[0]
        msg = 'Wifi al actief'
        print(msg)
        display.home()
        display.print(msg)
        
        display.setCursor(0, 1) # Cursor naar volgende regel
        msg = 'IP: ' + ipaddress
        print(msg)
        display.print(msg)
    else:
        wlan.active(True)
        wlan.connect(ssid, password)

        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            #end if
            led.on()
            max_wait -= 1
            print('Wachten op connectie...')
            sleep(1/2)
            led.off()
            sleep(1/2)
        #end loop

        if wlan.status() != 3:
            buzzer.soundError()
            msg = 'Verbinden met Wifi mislukt.'
            led.off()
            display.home()
            display.print(msg)
            raise RuntimeError(msg)
        else:
            led.on()
            status = wlan.ifconfig()
            soundOK()
            print('Verbonden met Wi-Fi netwerk %s. IP adres: %s' % (ssid, status[0]) )
            
            display.home()
            display.print('Wifi: Bifi')
            
            display.setCursor(0, 1) # Cursor naar volgende regel
            msg = 'IP: ' + status[0]
            display.print(msg)
        #end if
    #end if
#end def


def disconnect(ssid):
    if wlan.isconnected():
        ssid = wlan.config('ssid')
        wlan.disconnect() 
        wlan.active(False)
        print('Verbinding verbroken met Wi-Fi netwerk', ssid)
    else:
        status = wlan.status()
        print('Geen actieve verbinding met een Wi-Fi network.')
    #endif
    led.off()
#end def
    

def soundOff():    
    buzzer.duty_u16(0)
#end def


def soundDefault():
    buzzer.duty_u16(10000)    
    buzzer.freq(2000)
    sleep(0.1)
    buzzer.freq(1000)
    sleep(0.1)
    soundOff()
#end def


def soundOK():
    buzzer.duty_u16(10000)
    buzzer.freq(1000)
    sleep(0.1)
    buzzer.freq(2000)
    sleep(0.1)
    buzzer.freq(3000)
    sleep(0.1)    
    soundOff()
#end def
    

def soundError():
    buzzer.freq(2000)
    buzzer.duty_u16(10000)
    sleep(0.1)
    buzzer.freq(1000)
    sleep(0.2)
    soundOff()   
#end def
    

##############################################################################
# Main
##############################################################################

ssid = 'Bifi'
password = '@Donderdag1441'
connect(ssid, password)


# Open a socket for incoming connections
myAddress = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
mySocket = socket.socket()
mySocket.bind(myAddress)
mySocket.listen(1)
msg = 'Socket aangemaakt. URL: http://' + getIpAddress()
print(msg)


# Listen for connections
while True:
    try:
        connection, address = mySocket.accept()
        print('Connectie van IP adres', address[0])
        cl_file = connection.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
            #endif
        #endloop
        soundDefault()
        
        message = 'Hallo, je gebruikt IP adres ' + address[0]
        response = html % message
        
        connection.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        connection.send(response)
        connection.close()
    except OSError as e:
        connection.close()
        print('Socket connectie gesloten')
    #endtry
#endloop






