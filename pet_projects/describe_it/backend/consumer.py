import os, pika, time

def callback(ch, method, properties, body):
    print('CONSUMER CALLBACK START')
    print(os.environ.get('AMQP_QUEUE'))
    print(properties)
    print(body)
    print('CONSUMER CALLBACK FINISH\n\n\n')

amqp_conn_url = os.environ.get('AMQP_URL')
if not amqp_conn_url:
    amqp_conn_url='amqp://put_user:put_password@localhost:18003/%2F'

pika_params = pika.URLParameters(amqp_conn_url)
pika_params.heartbeat = 0
conn_attempts = 30
while conn_attempts > 0:
    conn_attempts -= 1
    try:
        pika_conn = pika.BlockingConnection(pika_params)
        conn_attempts = 0
    except pika.exceptions.AMQPConnectionError as e:
        print(amqp_conn_url)
        print('AMQPConnectionError. Attempts remaining: ' + str(conn_attempts))
        time.sleep(10)
ch = pika_conn.channel()

queue_name = os.environ.get('AMQP_QUEUE')
if not queue_name:
    queue_name = 'hello'

ch.queue_declare(queue=queue_name)
ch.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
ch.start_consuming()
