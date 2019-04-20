# -*- coding: utf-8 -*-

"""
1. Install rabbitmq:
    brew install rabiitmq

2. Install pika
    pipenv install pika

3. Start rabbitmq server
     brew service start rabbitmq/rabbitmq-server(add the path first)
"""
import pika
import time
import sys


def receive():
    # establish connection
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    chan = conn.channel()

    chan.exchange_declare(exchange='topic_logs', exchange_type='topic')
    # declare message_queue name
    # chan.queue_declare(message_queue='leo')
    # message_queue name '' means a random message_queue
    # exclusive means when the chan closed, delete the message_queue
    result = chan.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    # The messages will be lost if no message_queue is bound to the exchange yet
    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)
    for severity in severities:
        chan.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=severity)

    #  don't dispatch a new message to a worker until it has processed and acknowledged the previous one
    # chan.basic_qos(prefetch_count=1)

    # receive message and call a func to deal with it
    chan.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [Consumer] Waiting for messages. To exit press CTRL+C')

    chan.start_consuming()


def callback(ch, method, properties, body):
    # message handler
    print(' [Consumer] Received %r' % body)
    time.sleep(body.count(b'.'))
    print('[Consumer] Done')
    # ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    receive()
