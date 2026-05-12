#!/bin/bash

logitech_mouse_id=$(xinput list | grep "Logitech USB Receiver  " | sed 's/^.*id=\([0-9]*\)[ \t].*$/\1/')
if [ -z $logitech_mouse_id ]
then
    echo Logitech Mouse Not Found > /tmp/my_mouse_id.txt
else
    echo Device Id is > /tmp/my_mouse_id.txt
    echo $logitech_mouse_id >> /tmp/my_mouse_id.txt
    echo Original map is: 1 2 3 4 5 6 7 8 9 >> /tmp/my_mouse_id.txt
    echo Here right-click is 3, go-back is 8, and go-fwd is 9 >> /tmp/my_mouse_id.txt
    echo 1 2 9 4 5 6 7 3 8 sets go-fwd on right button, right-click on go-back button, and go-back on go-fwd button  >> /tmp/my_mouse_id.txt
    echo If like to double right-click on additional button: 1 2 3 4 5 6 7 3 8 >> /tmp/my_mouse_id.txt
    xinput set-button-map $logitech_mouse_id 1 2 3 4 5 6 7 3 8
fi

