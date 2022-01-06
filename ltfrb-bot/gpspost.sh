#!/bin/bash
read MESSAGE
get_curr () {
  echo "$MESSAGE" | awk '{split($0,a,"+"); for (key in a) if (a[key] ~ /'$1'/) split(a[key],out,"#"); print out[2]}'
}

psql -c \
    "INSERT INTO gpspoint(
    id, 
    date_created, 
    latitude, 
    longitude, 
    altitude, 
    speed, 
    course
    ) 

    VALUES (
    '$(get_curr 'ID')', 
    '$(get_curr 'DT') $(get_curr 'TM')', 
    '$(get_curr 'LT')', 
    '$(get_curr 'LN')', 
    '$(get_curr 'AT')', 
    '$(get_curr 'SP')', 
    '$(get_curr 'CO')'
    );
    " \
    -d adventure;

psql -c "SELECT * FROM gpspoint;" -d adventure;
#psql -c "DELETE FROM gpspoint WHERE id = '$(get_curr 'ID')'" -d adventure;
