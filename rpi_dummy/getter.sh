#!/bin/bash

source $1

cd $BASE_PATH/tempfiles
mkdir -p  videos;
> video_list_temp
> video_diff
> video_list

while :
do
  curl -X GET -s $BASE_URL/api/request/all \
    | jq -rc '.[] | .locname+"-"+(.userid|tostring)+"-"+(.id|tostring)+"-"+.videoname' \
    | sed 's/ /_/g' \
    | awk '!seen[$0]++' > video_list_temp


  awk 'NR==FNR{a[$0]=1;next}!a[$0]' video_list video_list_temp > video_diff
  if ! [ -s video_list ]; then cat video_list_temp >video_diff; else awk 'NR==FNR{a[$0]=1;next}!a[$0]' video_list video_list_temp > video_diff; fi
  while read localname; do
    fname=$(echo "$localname" | awk '{n=split($0,a,"-"); print a[n]}')
    wget --quiet -O $BASE_PATH/videos/$localname $BASE_URL/api/video/display/$(echo $fname) 
  done < video_diff

  cat video_list_temp >video_list
  sleep 20;
done
