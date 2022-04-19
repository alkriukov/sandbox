import os, pika, time, json

queue_title = os.environ.get('AMQP_QUEUE')
if not queue_title:
    queue_title = 'hello'

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

ch.queue_declare(queue=queue_title)

def publish(headers, body):
    pika_props = pika.BasicProperties(headers=headers)
    ch.basic_publish(exchange='',
        routing_key=queue_title,
        body=json.dumps(body),
        properties=pika_props)
    print('SENT')
