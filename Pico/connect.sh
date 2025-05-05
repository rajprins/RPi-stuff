#!/usr/bin/env bash
#
DEVICE=/dev/cu.usbmodem1101
#DEVICE=/dev/tty.usbmodem1101

#minicom -b 115200 -o -D $DEVICE

echo "Connecting to device $DEVICE"
rshell --buffer-size=30 -p $DEVICE -a