#!/bin/bash

logitech_mouse_id=$(xinput list | grep "Logitech USB Receiver  " | sed 's/^.*id=\([0-9]*\)[ \t].*$/\1/')
echo $logitech_mouse_id > /tmp/my_mouse_id.txt
xinput set-button-map $logitech_mouse_id 1 2 3 4 5 6 7 3 8

