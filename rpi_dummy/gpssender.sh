#!/bin/bash

BASE_DIR=/home/pi/Desktop/rpi_dummy
BASE_DIR=.
BASE_URL=192.168.254.115
BASE_URL=localhost
ID=1

cd $BASE_DIR/tempfiles

# Create file for location
if ! [ -f currentlocation ]; then touch  currentlocation; fi
>  currentlocation

while :
do

  #
  #
  #    RETRIEVE GPS HERE
  #
  #

  curl -X POST -s "$BASE_URL:5000/api/gps/id=$ID+lat=14.656556+lon=121.025599" \
      | jq -rc '.[] | .locname' \
      | sed 's/ /_/g' >  currentlocation
  sleep 0.5;
done
