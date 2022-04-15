FROM rabbitmq

ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

WORKDIR /app
COPY rabbit/ /app/
RUN chmod +x init.sh

CMD ./init.sh