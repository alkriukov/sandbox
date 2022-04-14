import os, pika
import queue

def callback_hello(ch, method, properties, body):
    print('Callback hello')

amqp_conn_url = os.environ.get('FLASK_AMQP_URL')
if not amqp_conn_url:
    amqp_conn_url='amqp://put_user:put_password@localhost:8003/%2F'

pika_params = pika.URLParameters(amqp_conn_url)
pika_params.heartbeat = 0
pika_conn = pika.BlockingConnection(pika_params)
ch = pika_conn.channel()

ch.queue_declare(queue='hello')
ch.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback_hello)
ch.start_consuming()
