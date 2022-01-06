#!/bin/bash

mkdir -p ./videos;

curl -X GET -s localhost:5000/api/request/all \
  | jq -rc '.[] | (.userid|tostring)+"-"+.videoname' \
  | awk '!seen[$0]++' > video_list

while read localname; do
  fname=$(echo "$localname" | awk '{split($0,a,"-"); print a[2]}')
  wget -O ./videos/$localname localhost:5000/api/video/display/$(echo $fname) 
done <video_list
