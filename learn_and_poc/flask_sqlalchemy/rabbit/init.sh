#!/bin/sh

rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE

rabbitmqctl add_user user pass
rabbitmqctl set_user_tags user administrator
rabbitmqctl set_permissions -p / user  ".*" ".*" ".*"

rabbitmq-server
