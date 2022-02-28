#!/bin/bash

#/bin/vlc-wrapper --loop /home/pi/Desktop/rpi_dummy/videos
figlet -f standard -c  "ARANGKADATA copyright 2022"
figlet -f mini -k  "Video player would start automatically in 10 seconds"
ctr=10

while [ $ctr -gt 0 ]
do
	echo Video player starting in $ctr seconds
	sleep 1;
	ctr=$(($ctr - 1))
done
exit 1;

#read -p "Press any button to continue"
#/usr/bin/python3 /home/pi/Desktop/rpi_dummy/1.py
/usr/bin/vlc --fullscreen --play-and-exit /home/pi/Desktop/rpi_dummy/videos/1-minecraft.mp4

#while read localname; do
#  vlc --fullscreen --play-and-stop ./videos/$localname
#done <video_list
