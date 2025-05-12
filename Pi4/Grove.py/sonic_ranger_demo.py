#!/usr/bin/env python
################################################################################
# Sonic Ranger moet worden aangesloten op poort D5
#
# Syntax: python3 sonic_ranger_demo.py <begin_score_in_CM>
# Voorbeeld: python3 sonic_ranger_demo.py 30
# 
# Let op:
# Zorg er voor dat bestand sonic_ranger_lib.py in dezelfde directory staat
################################################################################

import time
import os
import sys

from sonic_ranger_lib import GroveUltrasonicRanger

# Sonic Ranger wordt aangesloten op poort D5
_PORT = 5

# Controleer op programma argument
if len(sys.argv) < 2:
    print('Fout: geen begin score opgegeven!')
    print('Syntax: {} <begin_score_in_CM>'.format(sys.argv[0]))
    print('Voorbeeld: {} 30'.format(sys.argv[0]))
    sys.exit(1)

# Zet de eerste high score
hiscore = float(sys.argv[1])

# Start de sonic ranger
sonar = GroveUltrasonicRanger(int(_PORT))

# Start een loop
while True:
    os.system('clear') # scherm leegmaken
    afstand = sonar.get_distance() # meet afstand via sensor

    print('Beste score  : ',hiscore) # Toon de huidige high score
    print('Jouw afstand : ',afstand) # Toon de gemeten afstand

    # Indien nieuwe beste score 
    # (dus wanneer de gemeten afstand kleiner is dan de high score)
    if afstand < hiscore:
        print('\n*** NIEUWE HIGH SCORE! ***')
        hiscore = afstand # Zet de nieuwe high score naar de gemeten afstand

    # Wacht 1 seconde voor de volgende meting begint
    time.sleep(1)

