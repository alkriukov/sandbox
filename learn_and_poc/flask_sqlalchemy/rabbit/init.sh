#!/bin/sh

( rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user usermq usermqpass ; \
rabbitmqctl set_user_tags usermq administrator ; \
rabbitmqctl set_permissions -p / usermq  ".*" ".*" ".*" ; ) &
rabbitmq-server