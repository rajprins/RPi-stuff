#!/usr/bin/env bash

ARCHIVE=DietPi_RPi5-ARMv8-Bookworm.img.xz

if [[ -f $ARCHIVE ]]; then
    echo "File $ARCHIVE already exists. Please remove it or choose a different name."
    exit 1
fi

echo
echo ">>> Downloading DietPi for Raspberry Pi 5"
echo
wget -q https://dietpi.com/downloads/images/$ARCHIVE
if [ $? -ne 0 ]; then
    echo "Failed to download $ARCHIVE"
    exit 1
fi
echo "Download complete: $ARCHIVE"

echo
echo ">>> Unzipping $ARCHIVE"
#tar xJvf $ARCHIVE
unxz $ARCHIVE
if [ $? -ne 0 ]; then
    echo "Failed to unzip $ARCHIVE"
    exit 1
fi
echo "Unzipped to ${ARCHIVE%.xz}"

echo
echo "To write the image to an SD card, use the following command:"
echo "sudo dd if=${ARCHIVE%.xz} of=/dev/sdX bs=4M status=progress && sync"
echo "Replace /dev/sdX with your SD card device path."
echo "Make sure to unmount the SD card before running the dd command."
echo
echo "Script completed successfully."
echo "You can now safely eject the SD card and use it with your Raspberry Pi 5."
echo
