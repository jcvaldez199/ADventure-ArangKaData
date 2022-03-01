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

while IFS="" read -r p || [ -n "$p" ]
do

  #
  #
  #    RETRIEVE GPS HERE
  #
  
  LAT=$(printf '%s\n' "$p" | awk -F" " '{print $1}')
  LON=$(printf '%s\n' "$p" | awk -F" " '{print $2}')

  curl -X POST -s "$BASE_URL:5000/api/gps/id=$ID+lat=$LAT+lon=$LON" \
      | jq -rc '.[] | .locname' \
      | sed 's/ /_/g' >  currentlocation
  sleep 1;
done < EDSA_test
