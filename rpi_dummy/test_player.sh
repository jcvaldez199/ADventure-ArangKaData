#!/bin/bash

while read localname; do
  #omxplayer -o hdmi ./videos/$localname
  vlc --fullscreen --play-and-stop ./videos/$localname
done <video_list
