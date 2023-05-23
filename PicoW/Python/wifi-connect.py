from wifi import WIFI
from secrets import secrets

ssid = secrets['ssid']
password = secrets['password']

def main():
    wifi = WIFI()
    wifi.connect(ssid, password)

main()