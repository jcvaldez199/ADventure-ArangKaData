#!/bin/bash

source $1

cd $BASE_PATH/tempfiles

# Create file for location
if ! [ -f currentlocation ]; then touch  currentlocation; fi
>  currentlocation

while IFS="" read -r p || [ -n "$p" ]
do

  #
  #
  #    RETRIEVE GPS HERE
  #

  # RETRIEVE ID

  
  LAT=$(printf '%s' "$p" | awk -F" " '{printf $1}')
  LON=$(printf '%s' "$p" | awk -F" " '{printf $2}')
  URL="$BASE_URL/api/gps/id=$RPI_ID+lat=$LAT+lon=$LON"
  URL=${URL%$'\r'}

  curl -X POST -s $URL \
      | jq -rc '.[] | .locname' \
      | sed 's/ /_/g' >  currentlocation
  sleep 2.5;
done < EDSA_test
