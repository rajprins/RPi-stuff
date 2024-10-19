#!/usr/bin/env bash
#
#minicom -b 115200 -o -D /dev/cu.usbmodem101

rshell --buffer-size=30 -p /dev/tty.usbmodem1101 -a