#!/bin/bash

socat -u tcp-l:2000,fork system:./gpspost.sh
