#!/bin/sh

( rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user put_dev_user  put_dev_password ; \
rabbitmqctl add_user put_prod_user put_prod_password ; \
rabbitmqctl set_user_tags put_dev_user  administrator ; \
rabbitmqctl set_user_tags put_prod_user administrator ; \
rabbitmqctl set_permissions -p / put_dev_user  ".*" ".*" ".*" ; \
rabbitmqctl set_permissions -p / put_prod_user ".*" ".*" ".*" ) &
rabbitmq-server
