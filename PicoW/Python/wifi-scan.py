import network
import binascii

wlan = network.WLAN(network.STA_IF) 
wlan.active(True) 

print('Bezig met scannen van beschikbare draadloze netwerken...')
# Returns list of tuples with 6 fields: ssid, bssid, channel, RSSI, security, hidden
accessPoints = wlan.scan()
print('Gereed.\n')

#There are five values for 'security':
#0 – open
#1 – WEP
#2 – WPA-PSK
#3 – WPA2-PSK
#4 – WPA/WPA2-PSK
authmodes = ['Open', 'WEP', 'WPA-PSK', 'WPA2-PSK4', 'WPA/WPA2-PSK']


print('  |SSID           |BSSID (MAC)  |Ch |Signal |Security       ')
print('--+---------------+-------------+---+-------+---------------')

i=0
for (ssid, bssid, channel, rssi, authmode, hidden) in accessPoints:
    i+=1
    ssid = ssid.decode()
    bssid = binascii.hexlify(bssid).decode()
    authmode = authmodes[int(authmode)-1]
    print(f"{i:<2}|{ssid:<15}|{bssid:<13}|{channel:<3}|{rssi:<7}|{authmode:<15}")


