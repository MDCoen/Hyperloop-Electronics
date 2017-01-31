#!/bin/bash

if [ "$EUID" != "0" ]; then
	echo "Must be run as root user!"
fi

echo "BB-UART1" > /sys/devices/platform/bone_capemgr/slots
echo "BB-UART2" > /sys/devices/platform/bone_capemgr/slots

python ./hyperloop.py
