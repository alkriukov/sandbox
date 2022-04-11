#!/bin/sh

sleep 5

rabbitmqctl add_user user pass
rabbitmqctl set_user_tags user administrator
rabbitmqctl set_permissions -p / user  ".*" ".*" ".*"

rabbitmq-server
