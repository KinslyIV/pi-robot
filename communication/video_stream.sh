#!/bin/bash
rpicam-vid -t 0 \
    --width 640 --height 480 --framerate 25 \
    --codec h264 --inline --vflip --hflip \
    --nopreview \
    -o udp://192.168.1.126:5000

