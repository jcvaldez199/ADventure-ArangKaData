#!/bin/bash

BASE_DIR=.
BASE_DIR=/home/pi/Desktop/rpi_dummy
BASE_URL=localhost
BASE_URL=192.168.254.115

mkdir -p $BASE_DIR/videos;

while :
do
  curl -X GET -s $BASE_URL:5000/api/request/all \
    | jq -rc '.[] | (.userid|tostring)+"-"+.videoname' \
    | awk '!seen[$0]++' > $BASE_DIR/video_list_temp


  awk 'NR==FNR{a[$0]=1;next}!a[$0]' $BASE_DIR/video_list $BASE_DIR/video_list_temp > $BASE_DIR/video_diff
  while read localname; do
    fname=$(echo "$localname" | awk '{split($0,a,"-"); print a[2]}')
    wget --quiet -O $BASE_DIR/videos/$localname $BASE_URL:5000/api/video/display/$(echo $fname) 
    echo $localname
  done <$BASE_DIR/video_diff

  cat $BASE_DIR/video_list_temp > $BASE_DIR/video_list
  sleep 10;
done
