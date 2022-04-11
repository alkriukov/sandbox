FROM rabbitmq

WORKDIR /app
COPY rabbit/ /app/
RUN chmod +x init.sh

CMD ./init.sh