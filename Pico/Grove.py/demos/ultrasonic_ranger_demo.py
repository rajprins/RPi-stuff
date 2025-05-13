import time
from ultrasonic_ranger import GroveUltrasonicRanger

ultrasonic = GroveUltrasonicRanger(1)

while True:
    # measure distance in centimeters
    centimeters = ultrasonic.measureInCentimeters()
    print('centimeters {}'.format( centimeters ) )
    time.sleep_ms(1000)
    
    # measure distance in inches
    inches = ultrasonic.measureInInches()
    print('inches {}'.format( inches ) )
    time.sleep_ms(1000)