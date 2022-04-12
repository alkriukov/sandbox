#!/bin/sh

( rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user put_user put_password ; \
rabbitmqctl set_user_tags put_user administrator ; \
rabbitmqctl set_permissions -p / put_user  ".*" ".*" ".*" ) &
rabbitmq-server
