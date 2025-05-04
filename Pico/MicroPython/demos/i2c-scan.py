from machine import I2C,Pin

i2c0 = I2C(0,scl=Pin(9), sda=Pin(8), freq=400000)
i2c1 = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)

print('>>> Scanning i2c bus 0 for devices')
devices = i2c0.scan()
 
if len(devices) == 0:
    print("No i2c device found.")
else:
    print('i2c devices found:',len(devices))
 
for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))



print('>>> Scanning i2c bus 1 for devices')
devices = i2c1.scan()
 
if len(devices) == 0:
    print("No i2c device found.")
else:
    print('i2c devices found:',len(devices))
 
for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))

