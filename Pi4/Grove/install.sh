#!/usr/bin/env bash

GH_REPO=https://github.com/Seeed-Studio/grove.py.git
OS_ARCH=armhf

### Intro banner
clear
echo "+------------------------------------------------------------------------------+"
echo "|       Grove.py installatie script for Raspberry Pi 3/4 met 32-bits OS        |"
echo "+------------------------------------------------------------------------------+"


### Stap 1: Controleren op de juiste versie van Raspberry Pi OS (armhf)
echo
echo ">>> Bezig met controleren omgeving"
DETECTED_ARCH=$(dpkg --print-architecture)
if ! [[ $DETECTED_ARCH == $OS_ARCH ]] ; then
   echo "Fout: Dit is niet de 32-bits versie van Raspberry Pi OS!"
   echo "De Grove libraries zijn niet compatibel met het huidige besturingssysteem."
   echo "Installatie kan niet worden voortgezet."
   echo
   exit 1
else
   echo "OK."
fi


### Step 2: installeren van enkele dependencies"
echo
echo ">>> Installeren van benodige OS packages"

# Login wachtwoord is nodig voor sudo
echo -n "Geef het login wachtwoord van huidige gebruiker (${USER}): "
sudo -v
sudo apt install python3-virtualenv git -y


### Step 3: Downloaden en installeren van Grove.py libraries
echo
echo ">>> Installeren van Grove.py libraries"

# Directory git aanmaken indien deze niet bestaat
if ! [[ -d $HOME/git ]] ; then
   mkdir $HOME/git
fi
cd $HOME/git

# Grove.py github repo clonen
git clone $GH_REPO
cd grove.py

# Python virtuele omgeving aanmaken
virtualenv -p python3 env
source env/bin/activate

# Grove.py installeren via Pip
pip3 install .


### En klaar...
echo
echo "De Grove.py libraries zijn geinstalleerd voor de huidige gebruiker."
echo
