#!/bin/bash

BASE_DIR=.
BASE_DIR=/home/pi/Desktop/rpi_dummy
BASE_URL=127.0.0.1
BASE_URL=192.168.254.104
ID=1

cd $BASE_DIR/tempfiles

# Create file for location
if ! [ -f currentlocation ]; then touch  currentlocation; fi
>  currentlocation

while IFS="" read -r p || [ -n "$p" ]
do

  #
  #
  #    RETRIEVE GPS HERE
  #
  
  LAT=$(printf '%s' "$p" | awk -F" " '{printf $1}')
  LON=$(printf '%s' "$p" | awk -F" " '{printf $2}')
  URL="$BASE_URL:5000/api/gps/id=$ID+lat=$LAT+lon=$LON"
  URL=${URL%$'\r'}

  curl -X POST -s $URL \
      | jq -rc '.[] | .locname' \
      | sed 's/ /_/g' >  currentlocation
  sleep 2.5;
done < EDSA_test
