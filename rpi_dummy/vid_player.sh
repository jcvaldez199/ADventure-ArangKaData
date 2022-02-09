#!/bin/bash

while read localname; do
  omxplayer -o hdmi ./videos/$localname
done <video_list
