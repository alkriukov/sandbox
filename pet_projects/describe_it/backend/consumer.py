import os, pika, time, json
import backend_api
from flask import Response

class NoMatchToConsumerOperation(Exception):
    pass


def callback(ch, method, properties, body):
    print('CONSUMER CALLBACK START')
    print(os.environ.get('AMQP_QUEUE'))
    db_changed = False
    resp_text = ''
    resp_status = 200
    try:
        method = properties.headers['method']
        operation = properties.headers['operation']
        message_body = json.loads(body.decode('utf-8', errors='ignore'))
        request_args = message_body['request_args']
        request_data = message_body['request_body']
        print(method)
        print(operation)
        print(request_args)
        print(request_data)
        if operation == 'apiChangeTags':
            if 'tagname' not in request_args.keys():
                raise NoMatchToConsumerOperation('tagname missing from request arguments')
            response_info, db_changed = backend_api.apiChangeTags(method, request_data, request_args['tagname'])
        elif operation == 'apiChangeConnections':
            response_info, db_changed = backend_api.apiChangeConnections(method, request_data)
        elif operation == 'apiSetVotes':
            response_info, db_changed = backend_api.apiSetVotes(method, request_data)
        elif operation == 'apiVote':
            if 'up_or_down' not in request_args.keys():
                raise NoMatchToConsumerOperation('up_or_down missing from request arguments')
            response_info, db_changed = backend_api.apiVote(method, request_data, request_args['up_or_down'])
        else:
            raise NoMatchToConsumerOperation('Missing any matched consumer method')
        resp_text = response_info.response
        resp_status = response_info.status
    except NoMatchToConsumerOperation as e:
        resp_text = str(e.__class__.__name__) + ' ' + str(e)
        resp_status=400
    except Exception as e:
        resp_text = 'Cannot process request ' + str(e.__class__.__name__) + ' ' + str(e)
        resp_status = 500
    print(resp_text)
    print(resp_status)
    print('DB Changed: ' + str(db_changed))
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
