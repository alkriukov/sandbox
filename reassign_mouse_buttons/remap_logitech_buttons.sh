#!/bin/bash

logitech_mouse_id=$(xinput list | grep "Logitech USB Receiver  " | sed 's/^.*id=\([0-9]*\)[ \t].*$/\1/')
if [ -z $logitech_mouse_id ]
then
    echo Logitech Mouse Not Found > /tmp/my_mouse_id.txt
else
    echo $logitech_mouse_id > /tmp/my_mouse_id.txt
    xinput set-button-map $logitech_mouse_id 1 2 9 4 5 6 7 3 8
fi

