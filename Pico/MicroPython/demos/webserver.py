import time
import network
import machine
import sys
import socket
from secrets import secrets

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

led = machine.Pin("LED", machine.Pin.OUT)

# Load login data from different file for safety reasons
ssid = secrets['ssid']
password = secrets['password']

wlan = network.WLAN(network.STA_IF)


# Already connected?
if wlan.isconnected():
    ssid = wlan.config('ssid')
    print('Already connected to Wi-Fi named', ssid)
    sys.exit()
#endif


wlan.active(True) # Activate wifi module
wlan.config(pm = 0xa11140) # set power mode to get WiFi power-saving off (if needed)
wlan.connect(ssid, password) # Connect to wifi network


# Wait for connect
while not wlan.isconnected():
    print('Trying to connect to wifi...')
    led.on()
    time.sleep(1/2)
    led.off()
    time.sleep(1/2)
#endloop


# Handle connection error or timeout
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
    led.off()
else:
    led.on() # Turn on led to indicate that wifi is active
    status = wlan.ifconfig()
    ipaddress = status[0]
    print('Connected to Wi-Fi. IP adress: ',ipaddress)
#endif


# Open a socket for incoming connections
myAddress = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
mySocket = socket.socket()
mySocket.bind(myAddress)
mySocket.listen(1)
print('Socket created. URL: http://',ipaddress)


# Listen for connections
while True:
    try:
        connection, address = mySocket.accept()
        print('Client connected from IP address', address[0])
        cl_file = connection.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
            #endif
        #endloop
        
        message = 'Hello, world!'
        response = html % message
        
        connection.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        connection.send(response)
        connection.close()
    except OSError as e:
        connection.close()
        print('Socket connection closed')
    #endtry
#endloop

