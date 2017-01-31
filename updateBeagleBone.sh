#!/bin/bash

if [ "$1" == "" ]; then
	echo "Usage: updateBeagleBone [address]"
	exit 1
fi

rsync --progress -r --exclude *.swp --exclude=*.pyc ./beagleBone debian@"$1":/home/debian/

exit 0
