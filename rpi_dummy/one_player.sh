#!/bin/bash

BASE_DIR=/home/pi/Desktop/rpi_dummy
BASE_DIR=.

/bin/bash $BASE_DIR/getter.sh > /dev/null 2>&1 &
/bin/bash $BASE_DIR/test_sender.sh > /dev/null 2>&1 &
figlet -f standard -c  "ARANGKADATA copyright 2022"
figlet -f mini -k  "Video player would start automatically in 10 seconds"
ctr=10

while [ $ctr -gt 0 ]
do
	echo Video player starting in $ctr seconds
	sleep 1;
	ctr=$(($ctr - 1))
done

#read -p "Press any button to continue"
#/usr/bin/vlc --fullscreen --play-and-exit /home/pi/Desktop/rpi_dummy/videos/1-minecraft.mp4
/usr/bin/python3 $BASE_DIR/rpi_dummy/1.py > /dev/null 2>&1
