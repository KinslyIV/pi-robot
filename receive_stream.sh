#!/bin/bash
gst-launch-1.0 -v udpsrc port=5000     ! h264parse ! openh264dec ! videoconvert ! autovideosink sync=false

