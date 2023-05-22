from wifi import WIFI
from secrets import secrets

ssid = secrets['ssid']
password = secrets['password']

wifi = WIFI()
wifi.connect(ssid, password)