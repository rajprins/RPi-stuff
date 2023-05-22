# RPi-stuff

Various Raspberry Pi projects, demos and libraries.

## Projects

### PicoW
Demos and samples for the Raspberry Pi Pico W.

**Instructions**
1. Create a file named `secrets.py` in directory RPi-stuff/PicoW/Python.

2. The contents of this file will contain the credentials of the wifi network you want to use with you PicoW.

3. Add the following lines to this file:
```
secrets = {
    'ssid': 'MyWifiName',
    'password': 'MyPassword'
}
```
4. Change the values with your actual wifi name and password. Don't forget to save the file.
